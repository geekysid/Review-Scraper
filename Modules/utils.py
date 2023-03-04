#!/usr/local/bin/python3

# ## utiities functions to avoid code duplication

# ****** # # # # # # # # # # # # # # # # # # # # # # # ****** #
# ******                                               ****** #
# ******   Name: Siddhant Shah                         ****** #
# ******   Date: 04/03/2023                            ****** #
# ******   Desc: Review Scraper Utility Functions      ****** #
# ******   Email: siddhant.shah.1986@gmail.com         ****** #
# ******                                               ****** #
# ****** # # # # # # # # # # # # # # # # # # # # # # # ****** #


import os, pandas, pyfiglet, time, random, hashlib
from datetime import datetime
from Modules.db_connector import DBConnector
from urllib.parse import urlparse


DEBUG = True


# >> just for decoration
def intro():
    print()
    print(pyfiglet.figlet_format(" GeekySid"))
    print()
    print('  # # # # # # # # # # # # #  # # # # # # # #')
    print('  #                                        #')
    print('  #     REVIEW SCRAPER UILITY FUNCTIONS    #')
    print('  #           By: SIDDHANT SHAH            #')
    print('  #             Dt: 04-03-2023             #')
    print('  #      siddhant.shah.1986@gmail.com      #')
    print('  #    **Just for Educational Purpose**    #')
    print('  #                                        #')
    print('  # # # # # # # # # # # # #  # # # # # # # #')
    print()


# << function to add messages to console
def debug(message: str="", type: str="Info", logger=None):
    """function to add messages to console

    Args:
        message (str): message to be printed to console
        type (str): type of logger
        logger : logger to log into log file
    """

    if DEBUG == True:
        print(f" {message}")

    if logger:
        type == "exception" and logger.exception(message)
        type == "error" and logger.error(message)
        type == "warning" and logger.warning(message)
        type == "debug" and logger.debug(message)
        type == "info" and logger.info(message)


# << function called when script is terminated to update job status
def terminate_script(job_id: str, status:str, remarks: str="", logger=None):
    """function called when script is terminated to update job status

    Args:
        job_id (str): id of the job
        status (str): status to be updated
        remarks (str, optional): remarks to be added to job. Defaults to "".

    Returns:
        _type_: _description_
    """

    db_con = DBConnector()
    query = "UPDATE tb_jobs SET status='{}', remarks='{}' WHERE job_id='{}'".format(status, remarks, job_id)
    db_con.execute_insert_update(query, logger=logger)

    # TODO: update job table


# << function to convert datetime obj to string
def date_to_str(date_obj: datetime, date_format: str="%Y-%m-%d") -> str:
    """date_format: str="%Y-%m-%d"

    Args:
        date_obj (datetime): date that is required to convert to str
        date_format (str, optional): Format of date string. Defaults to "%Y-%m-%d".

    Returns:
        str: date in string format
    """
    try:
        return date_obj.strftime(date_format)
    except Exception as e:
        print(f" Cannot convert {date_obj} to string  || {e}")
        return ""


# << function to convert datetime obj to string
def date_from_str(string: datetime, date_format: str="%Y-%m-%d") -> datetime:
    """function to convert string to datetime.

    Args:
        string (str): string that is required to convert to date
        date_format (str, optional): Format of string. Defaults to "%Y-%m-%d".

    Returns:
        str: date in string format
    """

    try:
        return datetime.strptime(string.split(' ')[0], date_format)
    except Exception as e:
        print(f" Cannot convert {string} to datetime object as string is not in {date_format} format  || {e}")
        return ""


# << function to chekc if review_date falls between desired date range
def check_date_in_range(from_date: str, to_date: str, review_date: str, date_format: str="%Y-%m-%d"):
    """function to chekc if review_date falls between desired date range

    Args:
        from_date (str): lower limit of date range
        to_date (str): upper limit of the date range
        review_date (str): actual date of the review
        date_format (str, optional): date format. Default: %Y-%m-%d (2022-11-21)

    Returns:
        bool: True if review date falls between the range
    """

    from_date = date_from_str(from_date)
    to_date = date_from_str(to_date)
    review_date = date_from_str(review_date)
    return from_date <= review_date <= to_date


# << function to check if review_date falls below end_date
def check_date_below_range(from_date: str, review_date: str, date_format: str="%Y-%m-%d"):
    """function to chekc if review_date falls between desired date range

    Args:
        from_date (str): lower limit of date range
        review_date (str): actual date of the review
        date_format (str, optional): date format. Default: %Y-%m-%d (2022-11-21)

    Returns:
        bool: False if review date falls below the date range
    """

    from_date = date_from_str(from_date)
    review_date = date_from_str(review_date)
    return from_date > review_date


# << function to hash a string using sha256 algo
def hash256(string: str) -> str:
    """function to hash a string using sha256 algo

    Args:
        string (str): string that is needed to be hashed

    Returns:
        str: hashed string
    """

    hash_object = hashlib.sha256(string.encode())
    hash_value = hash_object.hexdigest()
    return hash_value


# << function to return domain from a url
def extract_domain(url: str) -> str:
    """function to extract domain from a given url

    Args:
        url (str): url

    Returns:
        str: doamin
    """

    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    return domain.replace("www.", "")  # Output: www.example.com


# << function to get source from DB from url
def get_source(url: str) -> str:
    """function that fetches matching source from DB depening on domain in url

    Args:
        url (str): url from which reviews are to be scraped

    Returns:
        str: sourve NAME
    """

    domain = extract_domain(url)
    source_query = "SELECT source_name FROM  tb_source WHERE LOWER(source_name)='{}'".format(domain.lower())
    source = DBConnector().execute_fetch(source_query, fetch_all=False)
    return source[0]


# << function to update job status
def update_job_status(job_id: int, new_status:str="", remarks:str="", execution_start_date: datetime=None, execution_end_date: datetime=None, logger=None) -> bool:
    """function that fetches matching source from DB depening on domain in url

    Args:
        job_id (int): if of the job
        new_status (str): new status that is required to be updated
        remarks (str, optional): remarks to be added to the job
        execution_start_date (datetime, optional): date when job was executed
        execution_end_date (datetime, optional): date when job ended

    Returns:
        bool:
    """

    try:
        update_params = ', '.join([ x for x in [
                "last_updated=now()",
                (new_status and f"status='{new_status}'") or "",
                (remarks and f"remarks='{remarks}'") or "",
                (execution_start_date and f"execution_start_date='{execution_start_date}'") or "",
                (execution_end_date and f"execution_end_date='{execution_end_date}'") or ""
            ] if x ])

        update_query = " UPDATE tb_jobs SET {} WHERE job_id={}; ".format(update_params, job_id)
        DBConnector().execute_insert_update(update_query)
        logger and debug(message=f"Job successfully Updated || Query: {update_query} ", type="info", logger=logger)
        return True
    except Exception as e:
        logger and debug(message=f"Unable to udpate job status (update_job_status) || Query: {update_query} || {e} ", type="exception", logger=logger)


# << function to make script pause for a random seconds
def random_sleep(lower_limit:int=3, upper_limit: int=7):
    """function to return a random number between upper and lower limit

    Args:
        lower_limit (int, optional): lowest number. Defaults to 3.
        upper_limit (int, optional): highest number. Defaults to 7.

    """
    time.sleep(random.randint(lower_limit, upper_limit))


# << funtion to get proxies and its authentication details from the csv and generate list of proxies
def get_proxies_from_csv(logger=None) -> list:
    """funtion to get proxies and its authentication details from the csv and generate list of proxies

    Returns:
        list: list of proxies with authentication
    """

    proxy_file = os.path.join(os.path.dirname(__file__), f"proxy.csv")
    # logger and logger.info(f"Fetching proxies from proxy file || {proxy_file}")

    if os.path.exists(proxy_file):
        df = pandas.read_csv(proxy_file)
        entries = df.to_dict("records")

        # logger and logger.debug(f"Fetched a total of {len(entries)} proxies.")
        return [{
            "http": f"http://{entry['username']}:{entry['password']}@{entry['URL']}:{entry['port']}"
        } for entry in entries]
    else:
        logger and logger.warning(f"Proxy file not found || {proxy_file}")


# << function to get a random proxy from a list of proxy
def get_random_proxy(logger=None) -> str :
    """function to get a random proxy from a list of proxy
    Returns:
        string: a random proxy
    """
    proxies = get_proxies_from_csv(logger=logger)
    if proxies:
        randomness = 0 if len(proxies) == 1 else random.randint(0, len(proxies)-1)
        return proxies[randomness]


# << function to save resposne in html file
def save_response_to_html(text: str, file: str) -> None:
    """saving response to th html file for future investigation

    Args:
        text (str): text from the response
        file (str): name of the file to save the path
    """

    html_path = os.path.abspath(os.path.dirname(__file__), "HTMLS")
    if not os.path.exists(html_path):
        os.makedirs(html_path)

    with open(os.path.join(html_path, file), "w", encoding="utf-8") as w:
        w.write(text)


# << function used to remove junks from text
def clean_text(text: str) -> str:
    if text:
        text = text.replace('\n', '').strip()
    else:
        text = ''
    return text