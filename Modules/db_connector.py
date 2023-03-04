#!/usr/local/bin/python3

# ## class that allows script to perform various database functions

# ****** # # # # # # # # # # # # # # # # # # # # # # # # # # ****** #
# ******                                                     ****** #
# ******   Name: Siddhant Shah                               ****** #
# ******   Date: 04/03/2023                                  ****** #
# ******   Desc: Review Scraper Database Function Script     ****** #
# ******   Email: siddhant.shah.1986@gmail.com               ****** #
# ******                                                     ****** #
# ****** # # # # # # # # # # # # # # # # # # # # # # # # # # ****** #


from dotenv import load_dotenv
from Modules import utils
import mysql.connector as MySql
import os, pyfiglet


# >> just for decoration
def intro():
    print()
    print(pyfiglet.figlet_format(" GeekySid"))
    print()
    print('  # # # # # # # # # # # # #  # # # # # # # #')
    print('  #                                        #')
    print('  #    REVIEW SCRAPER DATABASE FUNCTIONS   #')
    print('  #           By: SIDDHANT SHAH            #')
    print('  #             Dt: 04-03-2023             #')
    print('  #      siddhant.shah.1986@gmail.com      #')
    print('  #    **Just for Educational Purpose**    #')
    print('  #                                        #')
    print('  # # # # # # # # # # # # #  # # # # # # # #')
    print()



# Note: class that will be used to interact with the database
class DBConnector():
    def __init__(self):
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env')) # loading environment variables stored in .env file
        self.hostname = os.getenv('DB_HOST')
        self.database = os.getenv('DB_DATABASE')
        self.username = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')
        self.port = os.getenv('DB_PORT')


    # << function that allows connection to the server
    def create_db_connection(self, logger=None):
        """function used to make connection to the server

        Args:
            hostname (str): ip address of the server whenre DB is hosted
            database (str): name of t he DB
            username (str): username that will be used to log into DB
            password (str): password of the user used to connect to DB
            port (str): post on which DB will be listenning
        """
        try:
            connection = MySql.connect(host=self.hostname, user=self.username, password=self.password, database=self.database, port=self.port)
            cursor = connection.cursor()
            return connection, cursor
        except Exception as e:
            logger and utils.debug(message=f"Exception while connect to DB (create_db_connection) || {e}", type="exception", logger=logger)
            return None, None


    # << function to close the connection
    def close_db_connection(self, connection, cursor):
            """function used to close connection to the DB
            """
            if connection and cursor:
                cursor.close()
                connection.close()


    # << function to fetch results from the table
    def execute_fetch(self, query: str, fetch_all:bool=True, logger=None) -> list:
        """class function that allows user to fetch data from database for a given query

        Args:
            query (str): query that needs to be executeds
            fetch_all (str, optional): True if all recordsare to be returned

        Returns:
            list: result of executed
        """
        try:
            connection, cursor = self.create_db_connection()
            if connection and cursor:
                cursor.execute(query)
                result = cursor.fetchall() if fetch_all else cursor.fetchone()

        except Exception as e:
            logger and utils.debug(message=f"Exception while fetching data from DB (execute_fetch) || Query: {query} ||  {e}", type="exception", logger=logger)
            return []

        if connection and cursor:
            self.close_db_connection(connection, cursor)
            return result


    # << function to fetch results from the table
    def execute_insert_update(self, query: str, inserted_id: bool=False, logger=None) -> int:
        """class function that allows user to insert or update datat into DB depending on the query string

        Args:
            query (str): query that needs to be executed

        Returns:
            int: number of rows affected in DB
        """

        try:
            connection, cursor = self.create_db_connection()
            if connection and cursor:
                cursor.execute(query)
                connection.commit()
                result = (inserted_id and cursor.lastrowid) or cursor.rowcount
                if connection and cursor:
                    self.close_db_connection(connection, cursor)
                return result
        except Exception as e:
            logger and utils.debug(message=f"Exception while inserting/updaing data from DB (execute_insert_update) || Query: {query} ||  {e}", type="exception", logger=logger)
            return None


    # << function that allows to add/update bulk entries in DB
    def bulk_execution(self, query:str, data_to_execute: tuple, logger=None) -> int:
        """function used to insertor update in DB in bulk

        Args:
            query (str): query used for bulk insert
            data_to_execute (tuple): tuple of values to be inserted or updated to DB

        Returns:
            int: number of rows inserted or udpated
        """
        row_count = -1
        try:
            connection, cursor = self.create_db_connection()
            cursor.executemany(query, data_to_execute)
            row_count = cursor.rowcount
            connection.commit()
        except Exception as e:
            logger and utils.debug(message=f"Exception while bulk data from DB (bulk_execution) || Query: {query} ||  {e}", type="exception", logger=logger)
        if connection and cursor:
            self.close_db_connection(connection, cursor)

        return row_count

