#!/usr/local/bin/python3

# ## SCRAPER used to fetch Reviews from TripAdvisor.com


# ****** # # # # # # # # # # # # # # # # # # # # # # # ****** #
# ******                                               ****** #
# ******   Name: Siddhant Shah                         ****** #
# ******   Date: 04/03/2023                            ****** #
# ******   Desc: Reviews Scraper MAIN SCRAPER          ****** #
# ******   Email: siddhant.shah.1986@gmail.com         ****** #
# ******                                               ****** #
# ****** # # # # # # # # # # # # # # # # # # # # # # # ****** #


# >> imports
import argparse, datetime, sys, logging, os, time
from Modules import tripadvisor, utils, trustpilot, booking
from Modules.db_connector import DBConnector
from urllib.parse import urlparse


# Note: class to validate date received by user from argsparse
class ValidDateFormatAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            date = datetime.datetime.strptime(values, '%Y-%m-%d').date()
        except ValueError:
            raise argparse.ArgumentError(self, "Invalid date format. Use YYYY-MM-DD.")
        setattr(namespace, self.dest, date)


# Note: class to validate URL received by user from argsparse and make sure it belongs to one of the valid domains
class ValidUrlAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        valid_domains = ['trustpilot.com', 'tripadvisor.com', 'booking.com']
        self.valid_domains = kwargs.pop('valid_domains', valid_domains)
        super().__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            parsed_url = urlparse(values)
            if parsed_url.scheme and parsed_url.netloc:
                if any([parsed_url.netloc.endswith('.' + domain) or parsed_url.netloc == domain for domain in self.valid_domains]):
                    setattr(namespace, self.dest, values)
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            raise argparse.ArgumentError(self, "Invalid or unsupported URL formatMake sure url belongs to one fo these domains, booking.com, tripadvisor.com or trustpilot.com.")


# << function to add log file to the log_table
def add_log_file_to_table(log_file_name: str, job_id, logger):
    """function to add logfile to the the log table

    Args:
        log_file_name (str): name of the log file
        job_id (str): if og the job
    """

    download_path = os.path.join(os.path.dirname(__file__), 'Logs', log_file_name)
    query = f"INSERT INTO tb_logs (job_id, file_name, path_to_file, url_to_file, date_added) VALUES('{job_id}', '{log_file_name}', '{download_path}', '', CURRENT_TIMESTAMP);"
    result = DBConnector().execute_insert_update(query, logger=logger)
    if result:
        utils.debug(message=f"Added Log file to the Log Table", type="info", logger=logger)
    else:
        utils.debug(message=f"Failed to add Log file to the Log Table", type="warning", logger=logger)


# << function to get details from job table depending on job_id
def get_job_details(job_id: int) -> tuple:
    """function to get details from job table depending on job_id

    Args:
        job_id (int): id og the job

    Returns:
        tuple: url, from_date, to_date
    """

    try:
        query = "SELECT url, reviews_from_date, reviews_to_date, status, webhook_url FROM tb_jobs WHERE job_id='{}'".format(job_id)
        result = DBConnector().execute_fetch(query, fetch_all=False)
        if result:
            if result[3].lower() in [ 'added', 'queued' ]:
                return result[0], utils.date_to_str(result[1]), utils.date_to_str(result[2]), result[4]
            else:
                utils.debug(message=f"Job with ID {job_id}, has a status of {result[3]}. Can only process Jobs with status 'ADDED' or 'QUEUED'. Terminating Script", type="ERROR", logger=logger)
        utils.debug(message=f"No job found with given ID {job_id}. Terminating Script...", type="error", logger=logger)
    except Exception as e:
        utils.debug(message=f"Exception while fetching job details for job_id {job_id}\n{e}\n\nTerminating Script...", type="exception", logger=logger)
    return None, None, None, None


# << main function that does all task
# def main(job_id, url: str, from_date: str="2020-01-01", to_date: str=utils.date_to_str(datetime.datetime.now())):
def main(job_id, logger=None):
    """function that run scraper depending on the source in url

    Args:
        job_id (_type_): id of the job
        url (str): url from which reviews are to be scraped
        from_date (str, optional): date from which reviews are be scrape. Defaults to "2020-01-01".
        to_date (str, optional): date upto which reviews are be scrape. Defaults to Current Date.
    """

    if not logger:
        logger = set_logger(job_id=job_id)

    try:
        url, from_date, to_date, webhook_url = get_job_details(job_id)
        if url and from_date and to_date and webhook_url:
            # url, from_date, to_date, webhook_url = job_details
            if utils.update_job_status(job_id, new_status='RUNNING', execution_start_date=datetime.datetime.now(), logger=logger):
                if 'tripadvisor.com' in url:
                    tripadvisor.TripAdvisor(job_id=job_id, url=url, from_date=from_date, to_date=to_date, logger=logger)
                elif 'trustpilot.com' in url:
                    trustpilot.TrustPilot(job_id=job_id, url=url, from_date=from_date, to_date=to_date, logger=logger)
                elif 'booking.com' in url:
                    booking.Booking(job_id=job_id, url=url, from_date=from_date, to_date=to_date, logger=logger)

            if webhook_url:
                print(f"==== Webhook URL: {webhook_url}")
                utils.push_to_webhook(job_id, webhook_url)

    except Exception as e:
        utils.debug(message=f"Exception while running scrapers. \n{e}", type="exception", logger=logger)
    utils.debug(message=f"TERMINATING SCRIPT", type="debug", logger=logger)


# << function used to create job
def create_job(url: str, from_date: str="2020-01-01", to_date: str=utils.date_to_str(datetime.datetime.now()), webhook_url=None) -> int:
    """function used to create job

    Args:
        url (str): url from which reviews are to be scraped
        from_date (str, optional): date from which reviews are be scrape. Defaults to "2020-01-01".
        to_date (str, optional): date upto which reviews are be scrape. Defaults to Current Date.
        webhook_url (str, optional): URL to which reviews will be pushed once scraping is completed.

    Returns:
        int: id of the job created
    """

    try:
        source = utils.get_source(url)
        job_query = """
            INSERT INTO tb_jobs (url, source, reviews_from_date, reviews_to_date, status, date_added, webhook_url)
            VALUES('{}', '{}', '{}', '{}', 'ADDED', now(), '{}');
        """.format(url, source, utils.date_from_str(from_date), utils.date_from_str(to_date), webhook_url)
        job_id = DBConnector().execute_insert_update(job_query, inserted_id=True)
        if job_id:
            utils.debug(message=f"New Job created with id {job_id}", type="info", logger=logger)
        else:
            utils.debug(message=f"Failed to create new job (create_job)", type="exception", logger=logger)
        return job_id
    except Exception as e:
        utils.debug(message=f"Exception while creating new job\n{e}\n\nTerminating Script...", type="exception", logger=logger)


# << setting up logger
def set_logger(job_id=None):
    """function to setup logging int the project
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    logger_path = os.path.join(os.path.dirname(__file__), "Logs")
    if not os.path.exists(logger_path):
        os.makedirs(logger_path)

    if job_id: log_file = os.path.join(f"job-{job_id}__{datetime.datetime.now().strftime('%d-%m-%Y %H-%M-%S')}.log")
    else: log_file = f"{time.time()*100000}".split('.')[0] + ".log"

    file_handler = logging.FileHandler(os.path.join(logger_path, log_file))
    formatter = logging.Formatter("%(asctime)s - %(process)d - %(levelname)s - %(message)s", datefmt="%d-%m-%Y %H-%M-%S")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info(f"{os.path.basename(__file__)} || Time: {datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}  || JOB # {job_id}")
    if job_id:
        add_log_file_to_table(log_file, job_id, logger)
        return logger
    return logger, log_file


# << command line argument parser
def args_parser():
    """command line arguments parser

    Returns:
        parser: parser
    """
    parser = argparse.ArgumentParser(description="Arguments to the script")
    parser.add_argument(
        '--url',
        dest="url",
        required = True,
        action=ValidUrlAction,
        type = str,
        help = "\'URL\' of the property whose reviews are required",
    )
    parser.add_argument(
        "-s", "--start-date",
        dest="start_date",
        action=ValidDateFormatAction,
        help="Start Date in YYYY-MM-DD format",
        type = str
    )
    parser.add_argument(
        "-e", "--end-date",
        dest="end_date",
        action=ValidDateFormatAction,
        help="End Date in YYYY-MM-DD format",
        type = str
    )
    parser.add_argument(
        "-w", "--webhook",
        dest="webhook_url",
        type = str
    )
    return parser.parse_args()


if __name__ == '__main__':
    try:
        logger = None
        logger, log_file = set_logger()
        args = args_parser()
        job_id = create_job(url=args.url, from_date=utils.date_to_str(args.start_date), to_date=utils.date_to_str(args.end_date), webhook_url=args.webhook_url)
        # job_id = "165"
        if job_id:
            add_log_file_to_table(log_file, job_id, logger)
            main(job_id, logger=logger)

    except Exception as e:
        utils.debug(message=f"Exception while running scraper \n{e}", type="exception", logger=logger)

    logger and utils.debug(message=f"SCRIPT TERMINATED", type="info", logger=logger)
    logging.shutdown()
