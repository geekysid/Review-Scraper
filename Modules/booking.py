#!/usr/local/bin/python3

# ## SCRAPER used to fetch Reviews from TripAdvisor.com


# ****** # # # # # # # # # # # # # # # # # # # # # # # ****** #
# ******                                               ****** #
# ******   Name: Siddhant Shah                         ****** #
# ******   Date: 04/03/2023                            ****** #
# ******   Desc: Booking.com Reviews Scraper           ****** #
# ******   Email: siddhant.shah.1986@gmail.com         ****** #
# ******                                               ****** #
# ****** # # # # # # # # # # # # # # # # # # # # # # # ****** #


# >> imports
import json, pyfiglet, requests, cloudscraper
from scrapy import Selector
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
    print("  ", "#              BOOKING.COM             #")
    print("  ", "#          By: SIDDHANT SHAH           #")
    print("  ", "#            Dt: 03/03/2023            #")
    print("  ", "#     siddhant.shah.1986@gmail.com     #")
    print("  ", "#   **Just for Educational Purpose**   #")
    print("  ", "#                                      #")
    print("  ", '#'*40)
    print()


# Note: class that will be used to scrape reviews from TripAdvisor
class Booking(AbstractScraper):
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
        return {
            "Cookie": "_pxhd=d8XgqZqEI7wicbl6%252FrFEBO1LStgdprZpjQTsMZ4vgNifWb5qSrdXbM5IT19xab03eYOjf-M4pfqKsilRWN4S8w%253D%253D%253Apzt-X13LkDqjAWziN--%252FnEOhQ5aV54muOZUJbBm6YT31kfp5gRlC7lOrORjS2jfJ0vpYLHp-OjP3KO3eOu0klQkVtce4MULccalQnke07rY%253D; bkng=11UmFuZG9tSVYkc2RlIyh9YVdwkdr4wBU5dXMJACPBLzmG0glnTBiJEgsj1vhfkSTZHZaqJH5Y59%2BteWnj%2BHZCXjR5vfTVAUhfm2JjTon4a9LnCK7FiroZzQ%2B8nbISoW9ooMTXlqe9BCRMik1HZ6jin9r3VbgVyaVI8UUTnLP5%2FQNjcoKDV7LKv58ryQutAFmV1LQxR%2FsoaUg%3D; px_init=0"
        }


    # >> function to generate generic payload from location_id
    def generate_payload(self, review_offset: int=0) -> dict:
        """function to generate generic payload from location_id

        Args:
            review_offset (int): number from which next set of reviews are to be scraped

        Returns:
            dict: payload in dictionary format
        """

        return {}


    # >> function that lets reviews to be saved in database
    def add_reviews_to_db(self, reviews: list) -> bool:
        """ function that lets reviews to be saved in database

        Args:
            reviews (list): list of all reviews that are to be inserted into DB

        Returns:
            bool: true if success
        """

        bulk_insert_query = """
            INSERT IGNORE INTO m2websolution_db.tb_booking_reviews
            (job_id, published_date, reviewer_name, reviewer_country, room_type, stay_duration, stay_date, title, like_comment, dislike_comment, hotel_response, rating, likes, hash, scraped_date)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP);
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
                published_date = review.xpath(".//div[@class='c-review-block__row']/span[contains(@class, 'c-review-block__date')]//text()").extract_first().replace("Reviewed:", "").strip()
                published_date = datetime.strptime(published_date, "%d %B %Y")       # 1 February 2022
                published_date = datetime.strftime(published_date, "%Y-%m-%d")       # 2022-09-21
                review_date_valid = utils.check_date_in_range( self.from_date, self.to_date, published_date)
                published_date_below_range = utils.check_date_below_range( self.from_date, published_date)

                if review_date_valid:
                    review_dict = {"job_id": self.job_id, "published_date": published_date}
                    try:
                        review_dict['reviewer_name'] = review.xpath(".//span[contains(@class, 'bui-avatar-block__title')]/text()").extract_first().strip()
                    except:
                        review_dict['reviewer_name'] = ""
                    try:
                        review_dict['reviewer_country'] = review.xpath(".//span[contains(@class, 'bui-avatar-block__subtitle')]/text()").extract_first().strip()
                    except:
                        review_dict['reviewer_country'] = ""
                    try:
                        review_dict['room_type'] = review.xpath(".//a[contains(@class, 'c-review-block__stay-info-link')]//div/text()").extract_first().strip()
                    except:
                        review_dict['room_type'] = ""
                    try:
                        review_dict['stay_duration'] = review.xpath(".//li[contains(@class, 'c-review-block__stay-info-item')]//p/text()").extract_first().strip()
                    except:
                        review_dict['stay_duration'] = ""
                    try:
                        review_dict['stay_date'] = review.xpath(".//li[contains(@class, 'c-review-block__stay-info-item')]//span[@class='c-review-block__date']/text()").extract_first().strip()
                    except:
                        review_dict['stay_date'] = ""
                    try:
                        review_dict['title'] = review.xpath(".//h3[contains(@class, 'c-review-block__title')]/text()").extract_first().strip()
                    except:
                        review_dict['title'] = ""
                    try:
                        review_dict['like_comment'] = ""
                        review_dict['dislike_comment'] = ""

                        for comment in review.xpath(".//div[@class='c-review']/div[@class='c-review__row']"):
                            if 'Liked' in comment.xpath(".//span[@class='bui-u-sr-only']/text()").extract_first():
                                review_dict['like_comment'] = comment.xpath(".//span[@class='c-review__body']/text()").extract_first()
                            elif 'Disliked' in comment.xpath(".//span[@class='bui-u-sr-only']/text()").extract_first():
                                review_dict['dislike_comment'] = comment.xpath(".//span[@class='c-review__body']/text()").extract_first()
                    except:
                        pass
                    try:
                        review_dict['hotel_response'] = ' '.join([x.strip() for x in review.xpath(".//div[@class='c-review-block__response']//div[@class='c-review-block__response__inner']/span[last()]/text()").extract()]).replace("\n", "")
                    except:
                        review_dict['hotel_response'] = ""
                    try:
                        review_dict['rating'] = review.xpath(".//div[contains(@class, 'bui-review-score__badge')]/text()").extract_first().strip().replace("\n", "")
                    except:
                        review_dict['rating'] = ""
                    try:
                        review_dict['likes'] = ' '.join([x.strip() for x in review.xpath(".//p[contains(@class, 'review-helpful__vote-others-helpful')]//text()").extract()])
                    except:
                        review_dict['likes'] = ""

                    review_dict['hash'] = utils.hash256(json.dumps(review_dict))
                    processed_reviews.append(review_dict)

                if published_date_below_range:
                    break
            except Exception as e:
                utils.debug(message=f"Exception while processing review (process_reviews)\n{review}\n{e}", type="exception", logger=self.logger)

        return processed_reviews, published_date_below_range


    # >> function to process reviews and add to DB
    def process_reviews_add_to_db(self, reviews):
        if reviews:
            processed_reviews, published_date_below_range = self.process_reviews(reviews)     # process Reviews
    
            # if processed reviews is not empty list
            if processed_reviews:
                reviews_added = self.add_reviews_to_db(processed_reviews) # Save reviews to DB
                return reviews_added


    # >> function tp make API call and scrape reviews
    def scrape_reviews(self, html_text, offset) -> list:
        """function to scrape reviews from the response

        Args:
            response: response form the request

        Returns:
            list: reviews
        """
        try:
            selector = Selector(text=html_text)
            reviews = selector.xpath("//div[@class='c-review-block']")
            
            if len(reviews) > 0:
                utils.debug(message=f"Offset: {offset} || Reviews_count: {len(reviews)}", type="debug", logger=self.logger)
                return reviews, True
            else:
                utils.debug(message=f"Offset: {offset} || All reviews Scraped", type="debug", logger=self.logger)
                utils.terminate_script(job_id=self.job_id, status="COMPLETED", remarks="Scraped all required Reviews", logger=self.logger)
                utils.debug(message=f"Updated status of script to COMPLETED", type="debug", logger=self.logger)
                return False, False
        except Exception as e:
            utils.terminate_script(job_id=self.job_id, status="EXCEPTION", remarks=f"Exception while scraping reviews (scrape_reviews)\n{e}", logger=self.logger)
            utils.debug(message=f"Exception while scraping reviews (scrape_reviews)\n{e}", type="exception", logger=self.logger)
            return False, False


    # >> function to fetch total pages from response
    def get_total_pages(self, html_text):
        selector = Selector(text=html_text)
        pages_el = selector.xpath("//a[@class='bui-pagination__link']/span[1]/text()").extract()
        try:
            return (pages_el and int(pages_el[-1])) or 0
        except:
            return 0


    # >> function to make request to server to get reviews
    def get_response(self, url: str, offset: int=0):
        
        """_summary_

        Args:
            url (str): url of the request
            offset (int, optional): index of reviews to be loaded. Defaults to 0.

        Returns:
            response: response from the requests
        """
        try:
            utils.debug(message=f"Scraping reviews for Offset # {offset}", type="info", logger=self.logger)
            url = url.replace("__OFFSET__", str(offset))
            scraper = cloudscraper.create_scraper(
                delay=10, 
                browser={
                    'browser': 'chrome', 
                    'platform': 'android', 
                    'desktop': False, 
                }
            )

            # proxy = utils.get_random_proxy(self.logger)
            # if proxy is None:
            #     utils.terminate_script(job_id=self.job_id, status="ERRORED", remarks="Proxies not Found", logger=self.logger)
            #     utils.debug(message=f"No Proxies found. Terminating script...", type="errors", logger=self.logger)
            #     return None, False

            # response = requests.request("GET", url=url, proxies=proxy)

            result = scraper.get(url)
            utils.save_response_to_html(result.text, f"{self.job_id}__test.html")
            if result.status_code == 200:
                return result.text
            else:
                utils.debug(message=f"Got status code of {result.status_code} || URL: {url}", type="error", logger=self.logger)
                utils.terminate_script(job_id=self.job_id, status="Error", remarks=f"Got status code of {result.status_code} || URL: {url}", logger=self.logger)
        except Exception as e:
            utils.debug(message=f"Exception while getting response from 1st page. get_response() || {e}", type="exception", logger=self.logger)
            utils.terminate_script(job_id=self.job_id, status="Exception", remarks=f"Exception while getting response from 1st page. get_response() || {e}", logger=self.logger)


    # >> 
    def parse_input_link(self):
        page_name = self.url.replace(".html", "").replace(".htm", "").split("/")[-1].split(".")[0]
        return f"https://www.booking.com/reviewlist.en-gb.html?dist=1&pagename={page_name}&cc1=us&rows=25&=&type=total&offset=__OFFSET__"


    def main(self):
        try:
            offset = 0
            page_count = 0
            total_reviews_scraped = 0
            total_reviews_added_to_db = 0

            while True:
                target_site = self.parse_input_link()
                html_text = self.get_response(target_site, offset=offset)
                if offset == 0:
                    total_pages = self.get_total_pages(html_text)

                reviews, success  = self.scrape_reviews(html_text, offset)
                if not success:
                    return False

                if len(reviews) == 0:
                    utils.debug(message=f"All reviews({total_reviews_scraped}) scraped", type="info", logger=self.logger)
                    return None

                offset += len(reviews)
                reviews_added = self.process_reviews_add_to_db(reviews)
                total_reviews_added_to_db += reviews_added or 0
                utils.random_sleep()
                if page_count > total_pages:
                    utils.debug(message=f"All reviews({total_reviews_scraped}) scraped", type="info", logger=self.logger)
                    return None
                page_count += 1

        except Exception as e:
            utils.debug(message=f"Got exception in main function.\n{e}", type="exception", logger=self.logger)
            utils.terminate_script(job_id=self.job_id, status="Exception", remarks=f"Got exception in main function.\n{e}", logger=self.logger)
