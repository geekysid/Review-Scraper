#!/usr/local/bin/python3

# ## SCRAPER used to fetch Reviews from TripAdvisor.com


# ****** # # # # # # # # # # # # # # # # # # # # # # # ****** #
# ******                                               ****** #
# ******   Name: Siddhant Shah                         ****** #
# ******   Date: 04/03/2023                            ****** #
# ******   Desc: TrustPilot Reviews Scraper            ****** #
# ******   Email: siddhant.shah.1986@gmail.com         ****** #
# ******                                               ****** #
# ****** # # # # # # # # # # # # # # # # # # # # # # # ****** #


# >> imports
import json, pyfiglet, requests, sys
from datetime import datetime
from Modules import utils
import bs4 as bs
from Modules.db_connector import DBConnector
from Modules.abstract_scraper import AbstractScraper


# << just fro decoration
def intro_deco():
    print("\n")
    print(pyfiglet.figlet_format("  GeekySid"))
    print("\n")
    print("  ", '#'*40)
    print("  ", "#                                      #")
    print("  ", "#    Scraper to scrape REVIEWS from    #")
    print("  ", "#            TRUSTPILOT.COM            #")
    print("  ", "#          By: SIDDHANT SHAH           #")
    print("  ", "#            Dt: 03/03/2023            #")
    print("  ", "#     siddhant.shah.1986@gmail.com     #")
    print("  ", "#   **Just for Educational Purpose**   #")
    print("  ", "#                                      #")
    print("  ", '#'*40)
    print()


# Note: class that will be used to scrape reviews from TripAdvisor
class TrustPilot(AbstractScraper):
    def __init__(self, url: str="", from_date: str="2000-01-01", to_date: str="", job_id: str="", logger=None):
        self.url = url
        self.from_date = from_date      # lower limit of date range
        self.to_date = to_date or datetime.now().strftime("%Y-%m-%d")   # upper limit of the date range
        self.job_id = job_id
        self.logger = logger
        self.domain = utils.extract_domain(url)
        self.main()


    # >> return header to be used in API call
    @staticmethod
    def get_headers() -> dict:
        """function returns header to be used in API call

        Returns:
            dict:
        """
        return { "x-nextjs-data": "1" }


    # >> function to generate generic payload from location_id
    def generate_payload(self, review_offset: int=0) -> dict:
        """function to generate generic payload from location_id

        Args:
            review_offset (int): number from which next set of reviews are to be scraped

        Returns:
            dict: payload in dictionary format
        """

        return {}

    # >> function to process reviews and add to DB
    def process_reviews_add_to_db(self, reviews):
        reviews_added, published_date_below_range = None, True
        if reviews:
            processed_reviews, published_date_below_range = self.process_reviews(reviews)     # process Reviews

            # if processed reviews is not empty list
            if processed_reviews:
                reviews_added = self.add_reviews_to_db(processed_reviews) # Save reviews to DB

        return reviews_added, published_date_below_range



    # >> function to built endpoint to scrape reviews for pages > 1
    @staticmethod
    def parsed_input_link_to_json_endpoint(buildId, target_site, page):
        return f"https://www.trustpilot.com/_next/data/{buildId}/review/{target_site}.json?languages=all&page={page}&sort=recency&businessUnit={target_site}"


    # >> function tp make API call and scrape reviews
    def scrape_reviews(self, buildId: str, target_site: str, page: int) -> dict:
        """_summary_

        Args:
            buildId (str): unique identifier fetched from scraping 1st page
            target_site (str): url
            page (int): page number

        Returns:
            dict: api response
        """
        try:
            json_endpoint = self.parsed_input_link_to_json_endpoint(buildId, target_site, page)
            proxy = utils.get_random_proxy(self.logger)
            utils.debug(message=f"Page: {page} || URL: {json_endpoint}", type="debug", logger=self.logger)

            if proxy is None:
                utils.terminate_script(job_id=self.job_id, status="ERRORED", remarks="Proxies not Found", logger=self.logger)
                utils.debug(message=f"No Proxies found. Terminating script...", type="errors", logger=self.logger)
                return None, False

            try_count = 1
            while True:
                # utils.debug(message=f"Endpoint: {json_endpoint}", type="debug", logger=self.logger)
                response = requests.request("GET", url=json_endpoint, proxies=proxy, headers=self.get_headers(), data=self.generate_payload())
                if response.status_code == 200:
                    response_json = response.json()
                    reviews = ('pageProps' in response_json and  response_json['pageProps'] and 'reviews' in response_json['pageProps'] and response_json['pageProps']['reviews']) or []

                    if len(reviews) > 0:
                        utils.debug(message=f" >> Reviews_count: {len(reviews)}", type="debug", logger=self.logger)
                        return reviews, True
                    else:
                        utils.debug(message=f"  >> All reviews Scraped", type="debug", logger=self.logger)
                        utils.terminate_script(job_id=self.job_id, status="COMPLETED", remarks="Scraped all required Reviews", logger=self.logger)
                        utils.debug(message=f"Updated status of script to COMPLETED", type="debug", logger=self.logger)
                        return False, False
                else:
                    file = f"{self.domain.split('.')[0]}__{self.job_id}__page-{page}"
                    utils.save_response_to_html(response.text, file)
                    utils.debug(message=f"Got {response.status_code} status code", type="error", logger=self.logger)
                    try_count += 1
                    if try_count > 5:
                        utils.terminate_script(job_id=self.job_id, status="ERROR", remarks=f"Got {response.status_code} status code", logger=self.logger)
                        utils.debug(message=f"Unable to pull reviews. Getting status code: {response.status_code}. Check {file} file for more details", type="exception", logger=self.logger)
                        return False, False
        except Exception as e:
            utils.terminate_script(job_id=self.job_id, status="EXCEPTION", remarks=f"Exception while scraping reviews (scrape_reviews)\n{e}", logger=self.logger)
            utils.debug(message=f"Exception while scraping reviews (scrape_reviews)\n{e}", type="exception", logger=self.logger)
            return False, False


    # >> function that lets reviews to be saved in database
    def add_reviews_to_db(self, reviews: list) -> bool:
        """ function that lets reviews to be saved in database

        Args:
            reviews (list): list of all reviews that are to be inserted into DB

        Returns:
            bool: true if success
        """

        bulk_insert_query = """
            INSERT IGNORE INTO m2websolution_db.tb_trustpilot_reviews
            (job_id, trustpilot_id, published_date, rating, `text`, title, likes, consumer_name, user_info, reply, hash, scraped_date)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP);
        """
        params = [ tuple(review.values()) for review in reviews ]

        rows_affected = DBConnector().bulk_execution(bulk_insert_query, params, logger=self.logger)
        utils.debug(message=f"Added {rows_affected} out of {len(reviews)} reviews to the DB", type="debug", logger=self.logger)
        return rows_affected


    # >> function to process reviews
    def process_reviews(self, reviews: list) -> list:
        """function to process reviews

        Args:
            reviews (list): list of raw reviews that needs to be processed

        Returns:
            list: list of processed reviews
        """
        processed_reviews = []
        for review in reviews:
            try:
                published_date = review['dates']['publishedDate'].split('T')[0]
                review_date_valid = utils.check_date_in_range( self.from_date, self.to_date, published_date)
                published_date_below_range = utils.check_date_below_range( self.from_date, published_date)
                
                if review_date_valid:
                    review_data = {'job_id': self.job_id}
                    review_data['trustpilot_id'] = ("id" in review and review["id"]) or ""
                    review_data["published_date"] = published_date
                    review_data["rating"] = ("rating" in review and review['rating']) or ""
                    review_data["text"] = ("text" in review and review['text']) or ""
                    review_data["title"] = ("title" in review and review['title']) or ""
                    review_data['likes'] =  ("likes" in review and review["likes"]) or 0
                    review_data['consumer_name'] = ('consumer' in review and review['consumer'] and 'displayName' in review['consumer'] and review['consumer']['displayName']) or ""
                    review_data['user_info'] =  json.dumps(("consumer" in review and review["consumer"]) or {})
                    review_data['reply'] = json.dumps(("reply" in review and review["reply"]) or {})
                    review_data['hash'] = utils.hash256(json.dumps(review_data))
                    processed_reviews.append(review_data)

                if published_date_below_range:
                    break
            except Exception as e:
                utils.debug(message=f"Exception while processing review (process_reviews)\n{review}\n{e}", type="exception", logger=self.logger)

        return processed_reviews, published_date_below_range


    # >> function to get data script which will be used to get data using API
    def get_next_data_script_tag(self, page_soup):
        try:
            script_tag = page_soup.find('script', id='__NEXT_DATA__')
            # jsonStr = script_tag.text.strip()
            jsonStr = script_tag.next.strip()
            try:
                jsonObj = json.loads(jsonStr)
            except:
                utils.terminate_script(job_id=self.job_id, status="ERRORED", remarks=f"Not getting desired response in get_next_data_script_tag.", logger=self.logger)
                return False
            buildId = (jsonObj and 'buildId' in jsonObj and jsonObj['buildId']) or ""
            pageProps = (jsonObj and 'props' in jsonObj and jsonObj['props'] and 'pageProps' in jsonObj['props'] and jsonObj['props']['pageProps']) or {}
            reviews = (pageProps and 'reviews' in pageProps and pageProps['reviews']) or []
            totalPages = (pageProps and 'filters' in pageProps and pageProps['filters'] and 'pagination' in pageProps['filters'] and pageProps['filters']['pagination'] and 'totalPages' in pageProps['filters']['pagination'] and pageProps['filters']['pagination']['totalPages']) or ""

            return buildId, totalPages, reviews
        except Exception as e:
            utils.debug(message=f"Exception while getting data from script tag (get_next_data_script_tag()) || {e}", type="exception", logger=self.logger)
            utils.terminate_script(job_id=self.job_id, status="EXCEPTION", remarks=f"Got exception in get_next_data_script_tag function.\n{e}", logger=self.logger)
        return None, None, None


    # >> function to get response from the 1st page and returns soup
    def process_1st_page(self):
        url = self.url+"?languages=all&sort=recency"
        utils.debug(message=f"Scraping reviews from Page # 1  ||  {url}", type="info", logger=self.logger)
        for _ in range(5):
            try:
                proxy = utils.get_random_proxy(self.logger)
                response = requests.request("GET", url=url, proxies=proxy, headers={}, data={})
                if response.status_code == 200:
                    soup = bs.BeautifulSoup(response.text,'html.parser')
                    return soup 
            except Exception as e:
                utils.debug(message=f"Exception while getting response from 1st page. process_1st_page() || {e}", type="exception", logger=self.logger)
                return None


    # >> 
    def parse_input_link(self, buildId):
        business_url = self.url.split('/')[-1]
        self.url = f"https://www.trustpilot.com/_next/data/{buildId}/review/{business_url}.json?page=__PAGE__&businessUnit={business_url}"
        return business_url


    def main(self):
        try:
            total_reviews_scraped = 0
            total_reviews_added_to_db = 0
            page_soup = self.process_1st_page()          # function to get response from the 1st page and returns soup

            if not page_soup:
                utils.debug(message=f"Unable to get response from 1st Page || Terminating script", type="error", logger=self.logger)
                sys.exit()

            buildId, total_pages, reviews = self.get_next_data_script_tag(page_soup)
            target_site = self.parse_input_link(buildId)
            if reviews:
                total_reviews_scraped += (reviews and len(reviews)) or 0
                utils.debug(message=f"Total pages: {total_pages}", type="info", logger=self.logger)

                reviews_added, published_date_below_range = self.process_reviews_add_to_db(reviews)
                total_reviews_added_to_db += reviews_added or 0
                utils.random_sleep()

                # looping through all pages
                if total_pages > 1 and not published_date_below_range:
                    for page in range(2, total_pages):
                        utils.debug(message=f"Scraping reviews from Page # {page}", type="info", logger=self.logger)
                        reviews, success = self.scrape_reviews(buildId, target_site, page)
                        if not success:
                            return False
                        reviews_added, published_date_below_range = self.process_reviews_add_to_db(reviews)
                        total_reviews_scraped += (reviews and len(reviews)) or 0
                        total_reviews_added_to_db += reviews_added or 0
                        utils.random_sleep()
                        if published_date_below_range:
                            utils.debug(message=f"All reviews({total_reviews_scraped}) scraped from {total_pages} pages, for a given time frame ({self.from_date } to {self.to_date }) and {total_reviews_added_to_db} reviews added to DB", type="info", logger=self.logger)    
                            utils.terminate_script(job_id=self.job_id, status="COMPLETED", remarks=f"All reviews({total_reviews_scraped}) scraped from {total_pages} pages, for a given time frame ({self.from_date }", logger=self.logger)
                            return

                utils.debug(message=f"All reviews({total_reviews_scraped}) scraped from {total_pages} pages and {total_reviews_added_to_db} reviews added to DB", type="info", logger=self.logger)    
                utils.terminate_script(job_id=self.job_id, status="COMPLETED", remarks=f"All reviews({total_reviews_scraped}) scraped from {total_pages} pages and {total_reviews_added_to_db} reviews added to DB", logger=self.logger)
        except Exception as e:
            utils.debug(message=f"Got exception in main function.\n{e}", type="exception", logger=self.logger)
            utils.terminate_script(job_id=self.job_id, status="EXCEPTION", remarks=f"Got exception in main function.\n{e}", logger=self.logger)
