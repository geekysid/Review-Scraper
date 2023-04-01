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

            utils.terminate_script(job_id=self.job_id, status="ERRORED", remarks="Unable to extract location id from URL", logger=self.logger)
            utils.debug(message=f"Unable to extract location id from URL", type="error", logger=self.logger)
            return False
        except Exception as e:
            utils.terminate_script(job_id=self.job_id, status="ERRORED", remarks="Exception while getting location_id (extract_location_id)\n{e}", logger=self.logger)
            utils.debug(message=f"Exception while getting location_id (extract_location_id)\n{e}", type="exception", logger=self.logger)


    # << return header to be used in API call
    @staticmethod
    def get_headers() -> dict:
        """function returns header to be used in API call

        Returns:
            dict: 
        """

        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.tripadvisor.com/Hotel_Review-g150812-d754465-Reviews-or10-Rosewood_Mayakoba-Playa_del_Carmen_Yucatan_Peninsula.html',
            'content-type': 'application/json',
            'x-requested-by': 'TNI1625!AEbDTSnL3RR08cdKrUorfAQsRL5+XoWfhR6/ekV8Hlij8HSbDp1UT+QhfPFgP6zLHo0M/QT5gV9CicYi5d/hFyw9eKxW2JAe5RIZRiiF8N+bNGUcGozcjtzofK5kqZd/W7Kqv9RVdBxxiV4Zny6FMc76+1ElSEiTFqI2WVMSPN60',
            'Origin': 'https://www.tripadvisor.com',
            'Connection': 'keep-alive',
            'Cookie': 'datadome=3enDyV1cDxb~plA3Q8~TG7afkqkgm1XTmhdbhryjUjhje8txhHM0NmHmdwTd1Wlw5~q8m39xKGToibakec~Gqzr~iBER-j4KsAOXoaV1gzDu~edIBdu5b_Ccq3uBlay9; TADCID=X6iABE6ve5CCA95KABQCXdElnkGETRW-Svh01l3nWnSL8UJvJUzKQyZuLXFSNCcMp6Rymxtwyuh3702sYkc3sdjLii2nv1Ahchk; TAUnique=%1%enc%3AVk7jcyNIkdRFYb6CviSlwGuZ0AErVdEPSUBjoXrUqdvmhWnEwXwJZw%3D%3D; VRMCID=%1%V1*id.13092*llp.%2FHotels-a_cja%5C.12844798-a_cjp%5C.7753339-a_cjs%5C.242792d5562e69a6794f9439f0bd6813-m13092*e.1679168759988; _abck=A1877DE041951CD11DABDB7F0F277397~-1~YAAQb0xhaJ5yTRCHAQAAjtBvOwn3NbeE3VkTO9LOU5rKWzYCyCMS0s7sG/pN2PBV/oZ6FwAX4UK0Bn8a5TSzKcbU95biyVggUzynzJeDSxmicaltP9tKYHj4YXQLxsC6lqOByXrQrUkPgb6MSn7U9erj+5Hz4xk1JjVklVF6k3xXn6UbxXDc6Loqc+lzWwIoORJLzktFsrjveMTZYsHmfXHmdoLvcAInPsctGJFNi2oNFCby7axLjkcnhf5XVTeMIN8KW7fvVNNnN7Bc/QUcjDbXSH+dgaw6YRvEtT/1rtvWJvfJntJdulmbeGAfRkUkqAYFxJD3XaIFXUCUKNZyn+xf+u6jkm0V283Q02h3nt01gGw4EfPxLKeJqWa9xGuzWvjkopxyOt+/WaKnYhkN+w==~-1~-1~-1; TASSK=enc%3AAFgNWB%2B4SknqEn7cpvoxNKX58zI26iigGgqepWhsgwYKywRGNmy589AFy3Z79Df4RRQNQy1nZw7LqG80zkhcOKpOU8eBxpm1axtzDPYEky3AV%2F5mdmcYpJBTJPVjk8Mc7w%3D%3D; PAC=AOmtDzoMKT4V4_UP2UK5rY5_EZ2hutYx7g8AsZnlquf9ZhTZUVxOdbfnpgM2fy56gJ1MYFlJ4kDgDbkjL7zSuQDwt7v69KELnFaRXMpk-8Rpn0yUOgbuefvIcHQOx35O_g%3D%3D; PMC=V2*MS.57*MD.20230311*LD.20230401; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Apr+01+2023+11%3A40%3A09+GMT%2B0530+(India+Standard+Time)&version=202209.1.0&isIABGlobal=false&hosts=&consentId=fa3b1eed-483c-47ac-be94-9c14998bfc68&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; TATrkConsent=eyJvdXQiOiIiLCJpbiI6IkFMTCJ9; _pbjs_userid_consent_data=3524755945110770; _lc2_fpi=b140173de591--01gv93ax6nt17f2mhey1brb2k7; __gads=ID=87a7da0145152133:T=1678563965:S=ALNI_Ma1UUeaaqdanNj9-CYgHQsarxdlZw; __gpi=UID=00000bd792e35e7f:T=1678563965:RT=1680329402:S=ALNI_Mavnq7UROZq9kURCwnJynALXjUXtg; _lr_env_src_ats=false; TART=%1%enc%3ARWG%2Bgr4kpcDSDrdosbRI1zqhEaDsXjpnlHx5ItFwLlzFyXAKIqDkZUdvLNWJnAoHCVjgqw2ReXY%3D; TATravelInfo=V2*AY.2023*AM.4*AD.9*DY.2023*DM.4*DD.10*A.2*MG.-1*HP.2*FL.3*DSM.1680294043205*RS.1; TAUD=LA-1680294031395-1*RDD-1-2023_03_31*HDD-11696-2023_04_09.2023_04_10.1*LD-35377245-2023.4.9.2023.4.10*LG-35377247-2.1.F.; _lr_sampling_rate=100; pbjs_li_nonid=%7B%7D; ServerPool=C; _li_dcdm_c=.tripadvisor.com; BEPIN=%1%186d2359bdf%3Bweb303a.a.tripadvisor.com%3A30023%3B; TAReturnTo=%1%%2FHotel_Review-g150812-d754465-Reviews-Rosewood_Mayakoba-Playa_del_Carmen_Yucatan_Peninsula.html; TASession=V2ID.5BE34B5F0E8645B29C5175E41A35B1C5*SQ.93*LS.DemandLoadAjax*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.en*FA.1*DF.0*TRA.false*LD.754465*EAU._; __vt=tULUFSOZTLzx_-cRABQCwDrKuA05TCmUEEd0_4-PPCRr3nlBwRNXWKdVEKim26qF51_wSzXQz9X2S8_uSOx5y-Di4t7rVUVpdeQIG3_5gfd8pFrGXzinRmfqOohJcn1cNlLxqIj6AVGXh_KNydqzjaBzuOY; SRT=TART_SYNC; TASID=5BE34B5F0E8645B29C5175E41A35B1C5; ak_bmsc=841A5DD11A7C9FA16BE29E5F35BB10BB~000000000000000000000000000000~YAAQb0xhaJ9yTRCHAQAAjtBvOxPzc/9KMFt8Ud+jX4UupYYJ74GpFGnpPIkt9Nxoxzo9mVUpW/zfaj94ftCyOieRUOv+5EgXLjQT405m4W6i+kd+V5oS+xfJ/0McmthS9gbwl6+ajKXFlb/Qqv7HMGcyCkmjn1bs3LqMDOBKBXB0UsFgrWJP+IH5JJSYqFdF03JDakEyJtoBzAHU06WUUpKENVvJHww1EOMwUp4ZSBRex9LQUsL0gNDBIzJOE1FfwqU+tyioHssp7YWWYSLuk6AXdksU6/lKLNvRFOBdKZcnU3fCT3qUvPtJFVZU4JwcibAOTl7uw/nSiVsgnzAsu3L2b/N2z5CsApPYbn78OBVGeqGrzxoYECrVstul5AV9VF4H2nY+4j+KJseKemXyj8o=; bm_sz=50E74BABD3C26C2B21D17229CE1EA657~YAAQb0xhaKByTRCHAQAAjtBvOxOpXJC3qhjqpoJJIKiKaDMNbWZFGIyxwYRH7vAaoVyOuu2RT/LK5U5tRhL16xPP/0G6NLuAKGS599woIBC36W41ojXtjQRSDsr2btQxDlrtNzeQYpGOw8RctFudlM+nmA+GkMOd9qRirb0SI3zOjds++fRVsf4WZ5zZokR4cOtAzuqH898e5LpangFQuOp184nfIB4THBpi7OkGOi58ir3bRjFjQRf78TCu8wLL3y5UqiNk7RaTH7yrZNuByGX+z987+TX74hq7quJRHpMmFh16yjzSDA==~3224882~4407865; bm_sv=53458D9CFF2759193EF5568441149A96~YAAQb0xhaD52TRCHAQAAf1twOxPvmFS51aoPj2iuzhDsk85ijdKvZ10CNKyOx9thVkUIA2uT1P4oXgSA0A6dQjcTqEqew97ihVZW8pYmxDoLy/b/xtTbawax6l9unKL4AUVn7fUiq5H5EOXCu3ChnnRb03DqEkPrxPRNZl5hwerai+WKljbwdZlgxUqdt8Vdu7dzais+e6AXgc9Co+FTV7Fq/xAD6VM56GyiCxYCgTRtTgWzD7eomhR9pdMYUES+W2Nb9WFU~1; roybatty=TNI1625!ALu5b1Il4FpcQUO%2FWrP3x5JM0EFWqRUixAcfA9vfeV5M6NXxuCAHKDB7UT3OLJy61oUc3NurzWeU5e8%2FMJ0PzOAuFwo5eFeUUNaPmxww2zJCaqkspDBH8W%2BHZCLhNNPdIdvryLoggGb85oqVe6lUjdxbpPvXfLgYsO3Y9vJjCdE4%2C1; _lr_retry_request=true; TAUnique=%1%enc%3ARqJZljp%2F4CaHgzp8r%2BF783ih73RSUwb7ik7STkfu%2FB%2Fa%2B4A1Tt%2BEVA%3D%3D; _abck=800625D2858817C8177B3264DCD4B5E8~-1~YAAQjUxhaEBirgyHAQAA7qNvOwls2BuSVND3tF2oVJlmcVYw71pyikaf3JO+mbmSIcbjXAD3HMUoTM2XoseFq/jHdxfOJeJor/NdHVHRiy5Lpo0pTErC0CPoFvfeSWkQv2A2EPofdLhm9O+CrDlN3eu5yJMIwSB7AT9zzRwKEJaTomgHkjZLFuLpuE6Wn71VBMsUorGRfK8tNN1H3KQc/3OWaXMDrXISpW2hVqIkHVExlld60mnt9nb8/1K89PY6nnRciIXkc8U6mfUD8pn72aG29tbpcR6B9vAbGh9AjI8EbaDYShiVXeCxhkb7laEraP1iv/SdpYaffrDUuv5dA0g+Vc9G4WEsEnuFxkYJoRHdemLEOliVSl5WGkRBKg==~-1~-1~-1; bm_sz=5C3364BE1DA7721C578FD23D7892B48E~YAAQjUxhaEFirgyHAQAA7qNvOxNcjgWDqqiHOBCvBz0oZq/VWYDLHTI3UG2mhMB0a6oadLxLq2/Fu84y5ExnoAWYX2aqeQe16JyH9GbPtoTJTSyRjLe/nzpS8vho905Mf92gTXMLio+WTNYaWznZQ7cRQI/DFp1ziN7dPUJQOsa+usOxvVI1zSteipkVSKZmUTmCPkEKuKjM9uAqK8VQbQDfJeEZFMADhm2rhL+Qzo7EhFSGLeZlRmJIANbKrafriT8rxMzrxkeS1mb/iWwJjwSACg8SnDzNNShNdWU+KMJ4wp43kY8HZg==~4534597~4272441; TART=%1%enc%3Ah4M6fK%2Fhe%2FO%2FYYReZwAmtpW63wvC3VZceCWUaNfOe7lVowm89ljC3anYqkPP0qCgwgX04QEiDYc%3D; TASID=5BE34B5F0E8645B29C5175E41A35B1C5',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }


    # << function to generate generic payload from location_id
    def generate_payload(self, limit: int=50, review_offset: int=0) -> dict:
        """function to generate generic payload from location_id

        Args:
            review_offset (int): number from which next set of reviews are to be scraped
            limit (int): number reviews to get in each request

        Returns:
            dict: payload in dictionary format
        """

        # return [
        #     {
        #         "query": "e00c08246203980a6e31164c91047444",
        #         "variables": {
        #             "locationId": self.location_id,
        #             "limit": limit,
        #             "offset": review_offset,
        #             "routesRequest": []
        #         }
        #     }
        # ]

        return [{
            "query": "ea9aad8c98a6b21ee6d510fb765a6522",
            "variables": {
                "locationId": self.location_id,
                "offset": review_offset,
                "filters": [
                    {
                        "axis": "LANGUAGE",
                        "selections": [
                            "en"
                        ]
                    }
                ],
                "prefs": None,
                "initialPrefs": {},
                "limit": limit,
                "filterCacheKey": f"locationReviewFilters_{self.location_id}",
                "prefsCacheKey": f"locationReviewPrefs_{self.location_id}",
                "needKeywords": False,
                "keywordVariant": "location_keywords_v2_llr_order_30_en"
            }
        }]


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
                # Create a prepared request with the proxy settings
                response = requests.request("POST", proxies=proxy, url=url, headers=self.get_headers(), data=json.dumps(self.generate_payload(limit=self.review_limit_per_request, review_offset=review_offset)))

                if response.status_code == 200:
                    # with open('test.json', 'w') as w:
                    #     json.dump(response.json(), w, indent=4)

                    try:
                        resp_dict = response.json()[0]["data"]
                        locations = resp_dict and ("locations" in resp_dict and resp_dict["locations"] and resp_dict["locations"][0]) or ("locationReviews" in resp_dict and resp_dict["locationReviews"] and resp_dict["locationReviews"][0]) or {}
                        reviews = locations and "reviewListPage" in locations and locations["reviewListPage"] and "reviews" in locations["reviewListPage"] and locations["reviewListPage"]["reviews"] or []
                        # reviews = response.json()[0]["data"]["locationReviews"][0]
                    except Exception as e:
                        self.review_limit_per_request = int(self.review_limit_per_request/2)
                        if self.review_limit_per_request < 20:
                            file = f"{self.domain.split('.')[0]}__{self.job_id}__offset-{review_offset}"
                            utils.save_response_to_html(response.text, file)
                            raise Exception(f"Unable to get reviews with limit {self.review_limit_per_request} || {e}")
                        continue

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
                        utils.terminate_script(job_id=self.job_id, status="ERRORED", remarks=f"Got {response.status_code} status code", logger=self.logger)
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
            list: list of processed reviews
        """
        processed_reviews = []
        published_date_below_range = False
        for review in reviews:
            try:
                published_date = review['publishedDate']
                review_date_valid = utils.check_date_in_range( self.from_date, self.to_date, published_date )
                published_date_below_range = utils.check_date_below_range( self.from_date, published_date )
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

                if published_date_below_range:
                    break
            except Exception as e:
                utils.debug(message=f"Exception while processing review (process_reviews)\n{review}\n{e}", type="exception", logger=self.logger)

        return processed_reviews, published_date_below_range


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
            (job_id, tripadvisor_id, published_date, rating, `text`, title, username, user_info, publish_platform, provider_name, trip_info, social_statistics, owner_response, hash, scraped_date)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP);
        """
        params = [ tuple(review.values()) for review in reviews ]

        rows_affected = DBConnector().bulk_execution(bulk_insert_query, params, logger=self.logger)
        utils.debug(message=f"Added {rows_affected} out of {len(reviews)} reviews to the DB", type="debug", logger=self.logger)


    def main(self):
        self.location_id = self.extract_location_id()       # get location id from url
        if self.location_id:
            review_offset = 0
            self.review_limit_per_request = 200
            while True:
                try:
                    reviews = self.scrape_reviews(review_offset)
                    if reviews:
                        processed_reviews, published_date_below_range = self.process_reviews(reviews)     # process Reviews

                        # if processed reviews is not empty list
                        if processed_reviews:
                            self.add_reviews_to_db(processed_reviews) # Save reviews to DB

                        # if review date falls below date range then consider script as complete
                        if published_date_below_range:
                            utils.terminate_script(job_id=self.job_id, status="COMPLETE", remarks=f"Scraped all reviews for date greater than {self.from_date}", logger=self.logger)
                            utils.debug(message=f"Scraped all reviews for date great than {self.from_date}", type="debug", logger=self.logger)
                            break

                        review_offset += len(reviews)
                        utils.random_sleep(lower_limit=3, upper_limit=8)
                        continue
                except Exception as e:
                    utils.debug(message=f"Got exception in main function.\n{e}", type="exception", logger=self.logger)
                    utils.terminate_script(job_id=self.job_id, status="EXCEPTION", remarks=f"Got exception in main function.\n{e}", logger=self.logger)
                break

