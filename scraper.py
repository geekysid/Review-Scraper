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
import argparse, datetime, sys, logging, os
from Modules import tripadvisor, utils
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


# Note: class to validate URL received by user from argsparse and make sure it belogs to one of the valid domains
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
def add_log_file_to_table(log_file_name: str, logger):
    """functio to add logfile to the the log table

    Args:
        log_file_name (str): name of the log file
    """

    donwload_path = os.path.join(os.path.dirname(__file__), 'Logs', log_file_name)
    query = f"INSERT INTO m2websolution_db.tb_logs (job_id, file_name, path_to_file, url_to_file, date_added) VALUES('{job_id}', '{log_file_name}', '{donwload_path}', '', CURRENT_TIMESTAMP);"
    result = DBConnector().execute_insert_update(query, logger=logger)
    if result:
        utils.debug(message=f"Added Log file to the Log Table", type="info", logger=logger)
    else:
        utils.debug(message=f"Failed to add Log file to the Log Table", type="warning", logger=logger)


# << setting up logger
def set_logger():
    """funtion to setup logging int the project
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    logger_path = os.path.join(os.path.dirname(__file__), "Logs")
    if not os.path.exists(logger_path):
        os.makedirs(logger_path)

    log_file = os.path.join(f"job-{job_id}__{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    file_handler = logging.FileHandler(os.path.join(logger_path, log_file))
    formatter = logging.Formatter("%(asctime)s - %(process)d - %(levelname)s - %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info(f"{os.path.basename(__file__)} || Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    add_log_file_to_table(log_file, logger)
    return logger


# << command line argument parser
def args_parser():
    """command line arguments parser

    Returns:
        parser: parser
    """
    parser = argparse.ArgumentParser(description="Arguments to the script")
    parser.add_argument(
        "-j", "--job-id",
        dest="job_id",
        required = True,
        help="please enter job id",
        type = str
    )
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
    return parser.parse_args()


# << function to get details from job table depending on job_id
def get_job_details(job_id: int) -> tuple:
    """function to get details from job table depending on job_id

    Args:
        job_id (int): id og the job

    Returns:
        tuple: url, from_date, to_date
    """

    try:
        query = "SELECT url, reviews_from_date, reviews_to_date, status FROM tb_jobs WHERE job_id='{}'".format(job_id)
        result = DBConnector().execute_fetch(query, fetch_all=False)
        if result:
            if result[3].lower() in [ 'added', 'queued' ]:
                return result[0], utils.date_to_str(result[1]), utils.date_to_str(result[2])
            else:
                utils.debug(message=f"Job with ID {job_id}, has a status of {result[3]}. Can only process Jobs with status 'ADDED' or 'QUEUED'. Termnating Script", type="ERROR", logger=logger)
                return
        utils.debug(message=f"No job found with given ID {job_id}. Termnating Script...", type="error", logger=logger)
    except Exception as e:
        utils.debug(message=f"Exception while fetching job details for job_id {job_id}\,{e}\n\nTermnating Script...", type="exception", logger=logger)


# << main function thatt does all task
# def main(job_id, url: str, from_date: str="2020-01-01", to_date: str=utils.date_to_str(datetime.datetime.now())):
def main(job_id):
    """function that run scraper depedining on the source in url

    Args:
        job_id (_type_): id of the job
        url (str): url from which reviews are to be scraped
        from_date (str, optional): date from which reviews are be scrape. Defaults to "2020-01-01".
        to_date (str, optional): date upto which reviews are be scrape. Defaults to Current Date.
    """

    try:
        job_details = get_job_details(job_id)
        if job_details:
            url, from_date, to_date = job_details
            if 'tripadvisor.com' in url:
                if utils.update_job_status(job_id, new_status='RUNNING', execution_start_date=datetime.datetime.now(), logger=logger):
                    tripadvisor.TripAdvisor(job_id=job_id, url=url, from_date=from_date, to_date=to_date, logger=logger)
    except Exception as e:
        utils.debug(message=f"Exception while running scrapers. \n{e}", type="exception", logger=logger)
    utils.debug(message=f"TERMINATING SCRIPT", type="debug", logger=logger)


# << function used to create job
def create_job(url: str, from_date: str="2020-01-01", to_date: str=utils.date_to_str(datetime.datetime.now())) -> int:
    """function used to create job

    Args:
        url (str): url from which reviews are to be scraped
        from_date (str, optional): date from which reviews are be scrape. Defaults to "2020-01-01".
        to_date (str, optional): date upto which reviews are be scrape. Defaults to Current Date.

    Returns:
        int: id of the job created
    """

    try:
        source = utils.get_source(url)
        job_query = """
            INSERT INTO tb_jobs (url, source, reviews_from_date, reviews_to_date, status, date_added)
            VALUES('{}', '{}', '{}', '{}', 'ADDED', now());
        """.format(url, source, utils.date_from_str(from_date), utils.date_from_str(to_date))
        job_id = DBConnector().execute_insert_update(job_query, inserted_id=True)
        return job_id
    except Exception as e:
        print(f" Exception while trying to create job || {e}")


if __name__ == '__main__':
    try:
        args = args_parser()
        job_id = create_job(url=args.url, from_date=utils.date_to_str(args.start_date), to_date=utils.date_to_str(args.end_date))
        # job_id = 16
        if job_id:
            logger = set_logger()
            main(job_id)

    except Exception as e:
        print(f"Exception in argspase | {e}")

