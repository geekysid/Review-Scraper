import abc


# Note: Absract Class that will be inherited by by all scrapers
class AbstractScraper(metaclass=abc.ABCMeta):

    # << generating location id from the url
    @abc.abstractmethod
    def extract_location_id(self):
        pass


    # << function tp make API call and scrape reviews
    @abc.abstractmethod
    def scrape_reviews(self, review_offset: int) -> dict:
        pass


    # << function to process reviews
    @abc.abstractmethod
    def process_reviews(self, reviews: list) -> list:
        pass


    # << function that lets reviews to be saved in database
    @abc.abstractmethod
    def add_reviews_to_db(self, reviews: list) -> bool:
        pass


    @abc.abstractmethod
    def main(self):
        pass


    @abc.abstractmethod
    def extract_location_id(self):
        pass

