#!/usr/local/bin/python3

# ## SCRAPER used to fetch Reviews from TripAdvisor.com


# ****** # # # # # # # # # # # # # # # # # # # # # # # ****** #
# ******                                               ****** #
# ******   Name: Siddhant Shah                         ****** #
# ******   Date: 04/03/2023                            ****** #
# ******   Desc: TripAdvisor Reviews Scraper           ****** #
# ******   Email: siddhant.shah.1986@gmail.com         ****** #
# ******                                               ****** #
# ****** # # # # # # # # # # # # # # # # # # # # # # # ****** #


# >> imports
import json, pyfiglet, requests
from datetime import datetime
from Modules import utils
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
    print("  ", "#            TRIPADVIDOR.COM           #")
    print("  ", "#          By: SIDDHANT SHAH           #")
    print("  ", "#            Dt: 03/03/2023            #")
    print("  ", "#     siddhant.shah.1986@gmail.com     #")
    print("  ", "#   **Just for Educational Purpose**   #")
    print("  ", "#                                      #")
    print("  ", '#'*40)
    print()


# Note: class that will be used to scrape reviews from TripAdvisor
class TripAdvisor(AbstractScraper):
    def __init__(self, url: str="", from_date: str="2000-01-01", to_date: str="", job_id: str="", logger=None):
        self.url = url
        self.from_date = from_date      # lower limit of date range
        self.to_date = to_date or datetime.now().strftime("%Y-%m-%d")   # upper limit of the date range
        self.job_id = job_id
        self.logger = logger
        self.domain = utils.extract_domain(url)
        self.main()


    # << generating location id from the url
    def extract_location_id(self) -> str:
        """function to extract location id from the url

        Returns:
            str: location id
        """
        try:
            for part in self.url.split('-'):
                if part.startswith('d'):
                    location_Id = part.replace('d', '')
                    if location_Id.isdigit():
                        utils.debug(message=f"Location Id: {location_Id}", type="info", logger=self.logger)
                        return location_Id

            utils.terminate_script(job_id=self.job_id, status="ERROR", remarks="Unable to extract location id from URL", logger=self.logger)
            utils.debug(message=f"Unable to extract location id from URL", type="error", logger=self.logger)
            return False
        except Exception as e:
            utils.terminate_script(job_id=self.job_id, status="ERROR", remarks="Exception while getting location_id (extract_location_id)\n{e}", logger=self.logger)
            utils.debug(message=f"Exception while getting location_id (extract_location_id)\n{e}", type="exception", logger=self.logger)


    # << return header to be used in API call
    @staticmethod
    def get_headers() -> dict:
        """function returns header to be used in API call

        Returns:
            dict: 
        """

        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'content-type': 'application/json',
            'x-requested-by': 'TNI1625^!ALrRQOVySGV+HrqWI0C32dBjGs764Nw+kH2pDyl5PSlKhGeHGPC5rRVQ1dBXffQnew4pP+ooVY74QNUHpWb+TL3EgvwxIGK3psvBnjqQsDZ/48zQ8NWuWaIWIPl357ApLonnvdDxL0lWmgJL/41UP2t5DgvUD9Bcxgm8Q1Q6L1VC',
            'Origin': 'https://www.tripadvisor.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }


    # << function to generate generic payload from location_id
    def generate_payload(self, review_offset: int=0) -> dict:
        """function to generate generic payload from location_id

        Args:
            review_offset (int): number from which next set of reviews are to be scraped

        Returns:
            dict: payload in dictionary format
        """

        return [
            {
                "query": "e00c08246203980a6e31164c91047444",
                "variables": {
                    "locationId": self.location_id,
                    "limit": 750,
                    "offset": review_offset,
                    "routesRequest": []
                }
            }
        ]


    # << function tp make API call and scrape reviews
    def scrape_reviews(self, review_offset: int) -> dict:
        """_summary_

        Args:
            review_offset (int): number from which next set of reviews are to be scraped

        Returns:
            dict: api response
        """
        try:
            url = "https://www.tripadvisor.com/data/graphql/ids"
            proxy = utils.get_random_proxy(self.logger)

            if proxy is None:
                utils.terminate_script(job_id=self.job_id, status="ERRORED", remarks="Proxies not Found", logger=self.logger)
                utils.debug(message=f"No Proxies found. Terminating script...", type="errors", logger=self.logger)
                return None

            try_count = 1
            while True:
                response = requests.request("POST", proxies=proxy, url=url, headers=self.get_headers(), data=json.dumps(self.generate_payload(review_offset=review_offset)), stream=True)
                try:
                    ip_address = response.raw._original_response.fp.raw._sock.getpeername()[0]
                    utils.debug(message=f"IP Used: {ip_address}", type="info", logger=self.logger)
                except:
                    pass

                if response.status_code == 200:
                    reviews = response.json()[0]["data"]["locationReviews"][0]
                    if len(reviews) > 0:
                        utils.debug(message=f"Offset: {review_offset} || Reviews_count: {len(reviews)}", type="debug", logger=self.logger)
                        return reviews
                    else:
                        utils.debug(message=f"Offset: {review_offset} || All reviews Scraped", type="debug", logger=self.logger)
                        utils.terminate_script(job_id=self.job_id, status="COMPLETED", remarks="Scraped all required Reviews", logger=self.logger)
                        utils.debug(message=f"Updated status of script to COMPLETED", type="debug", logger=self.logger)
                        return False
                else:
                    file = f"{self.domain.split('.')[0]}__{self.job_id}__offset-{review_offset}"
                    utils.save_response_to_html(response.text, file)
                    utils.debug(message=f"Got {response.status_code} status code", type="error", logger=self.logger)
                    try_count += 1
                    if try_count > 5:
                        utils.terminate_script(job_id=self.job_id, status="ERROR", remarks=f"Got {response.status_code} status code", logger=self.logger)
                        utils.debug(message=f"Unable to pull reviews. Getting status code: {response.status_code}. Check {file} file for more details", type="exception", logger=self.logger)
                        break

        except Exception as e:
            utils.terminate_script(job_id=self.job_id, status="EXCEPTION", remarks=f"Exception while scraping reviews (scrape_reviews)\n{e}", logger=self.logger)
            utils.debug(message=f"Exception while scraping reviews (scrape_reviews)\n{e}", type="exception", logger=self.logger)


    # << function to process reviews
    def process_reviews(self, reviews: list) -> list:
        """function to process reviews

        Args:
            reviews (list): list of raw reviews that needs to be processed

        Returns:
            list: list of proccessed reviews
        """
        processed_reviews = []
        published_date_below_below_range = False
        for review in reviews:
            try:
                published_date = review['publishedDate']
                review_date_valid = utils.check_date_in_range( self.from_date, self.to_date, published_date )
                published_date_below_below_range = utils.check_date_below_range( self.from_date, published_date )
                if review_date_valid:
                    review_data = {'job_id': self.job_id}
                    review_data["tripadvisor_id"] = ("id" in review and review["id"]) or ""
                    review_data["published_date"] = published_date
                    review_data["rating"] = ("rating" in review and review['rating']) or ""
                    review_data["text"] = ("text" in review and review['text']) or ""
                    review_data["title"] = ("title" in review and review['title']) or ""
                    review_data['username'] =  ("username" in review and review["username"]) or ""
                    review_data['user_info'] =  ("userProfile" in review and review["userProfile"] is not None and "displayName" in review["userProfile"] and review["userProfile"]["displayName"]) or ""
                    review_data["publish_platform"] = ("publishPlatform" in review and review['publishPlatform']) or ""
                    review_data["provider_name"] = ("providerName" in review and review['providerName']) or ""
                    review_data["trip_info"] = json.dumps(("tripInfo" in review and review['tripInfo']) or {})
                    review_data["social_statistics"] = json.dumps(("socialStatistics" in review and review['socialStatistics']) or {})
                    review_data['owner_response'] =  json.dumps(("ownerResponse" in review and review["ownerResponse"] is not None and {
                        "title": ("title" in review["ownerResponse"] and review["ownerResponse"]['title']) or "",
                        "text": ("text" in review["ownerResponse"] and review["ownerResponse"]['text']) or "",
                        "publishedDate": ("publishedDate" in review["ownerResponse"] and review["ownerResponse"]['publishedDate']) or "",
                        "username": ("username" in review["ownerResponse"] and review["ownerResponse"]['username']) or ""
                    }) or { "title": "", "text": "", "publishedDate": "", "username": "" })
                    review_data['hash'] = utils.hash256(json.dumps(review_data))
                    processed_reviews.append(review_data)

                if published_date_below_below_range:
                    break
            except Exception as e:
                utils.debug(message=f"Exception while processing review (process_reviews)\n{review}\n{e}", type="exception", logger=self.logger)

        return processed_reviews, published_date_below_below_range


    # << function that lets reviews to be saved in database
    def add_reviews_to_db(self, reviews: list) -> bool:
        """ function that lets reviews to be saved in database

        Args:
            reviews (list): list of all reviews that are to be inserted into DB

        Returns:
            bool: true if success
        """

        bulk_insert_query = """
            INSERT IGNORE INTO m2websolution_db.tb_tripadvisor_reviews
            (job_id, tripadvisor_id, published_date, rating, `text`, title, username, user_info, publish_platform, provider_name, trip_info, social_statistics, owner_response, hash, scraped_data)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP);
        """
        params = [ tuple(review.values()) for review in reviews ]

        rows_affected = DBConnector().bulk_execution(bulk_insert_query, params, logger=self.logger)
        utils.debug(message=f"Added {rows_affected} out of {len(reviews)} reviews to the DB", type="debug", logger=self.logger)


    def main(self):
        self.location_id = self.extract_location_id()       # get location id from url
        if self.location_id:
            review_offset = 0
            while True:
                try:
                    reviews = self.scrape_reviews(review_offset)
                    if reviews:
                        processed_reviews, published_date_below_below_range = self.process_reviews(reviews)     # process Reviews

                        # if proccessed reviews is not emplt list
                        if processed_reviews:
                            self.add_reviews_to_db(processed_reviews) # Save reviews to DB

                        # if review date falls below date range then consider script as complete
                        if published_date_below_below_range:
                            utils.terminate_script(job_id=self.job_id, status="COMPELET", remarks=f"Scraped all reviews for date greate than {self.from_date}", logger=self.logger)
                            utils.debug(message=f"Scraped all reviews for date greate than {self.from_date}", type="debug", logger=self.logger)
                            break

                        review_offset += len(reviews)
                        utils.random_sleep(lower_limit=3, upper_limit=8)
                        continue
                except Exception as e:
                    utils.debug(message=f"Got exception in main function.\n{e}", type="exception", logger=self.logger)
                    utils.terminate_script(job_id=self.job_id, status="Exception", remarks=f"Got exception in main function.\n{e}", logger=self.logger)
                break

