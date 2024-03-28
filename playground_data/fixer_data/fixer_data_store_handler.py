# pylint: disable=C0116,R1710
"""
Implementation of persistent data store handler for Fixer API
"""

import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Generator

import pandas as pd
from dotenv import load_dotenv

from playground_data.abstract_data import DataStoreHandler


def daterange(date1: datetime, date2: datetime) -> Generator:
    """
    Generator which yields dates which are between the the two dates
    given.

    Args:
        date1 (datetime): start date
        date2 (datetime): end date

    Yields:
        Generator: yields datetime objects
    """
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)


class FixerDataStoreHandler(DataStoreHandler):
    """
    Class definition
    """

    def __init__(self):
        """
        Loads environment variables
        """
        super().__init__()
        env_path = Path("test.env")
        load_dotenv(dotenv_path=env_path)
        self.conn_info = {"DB_FILE": os.getenv("DB_FILE")}

    @property
    def conn_info(self):
        return self._conn_info

    @conn_info.setter
    def conn_info(self, val):
        self._conn_info = val

    @property
    def db_cursor(self):
        return self._db_cursor

    @db_cursor.setter
    def db_cursor(self, val):
        self._db_cursor = val

    @property
    def db_conn(self):
        return self._db_conn

    @db_conn.setter
    def db_conn(self, val):
        self._db_conn = val

    def open_connection(self, opt=None) -> None:
        """
        Creates database cursor and connection objects for the instance.

        Args:
            opt (_type_, optional): Defaults to None.

        Returns:
            None
        """

        try:
            db_conn = sqlite3.connect(self.conn_info.get("DB_FILE"))
            self.db_conn = db_conn
            self.db_cursor = self.db_conn.cursor()
        except sqlite3.Error as e:
            print(e)
            if self.db_conn:
                self.close_connection()

    def close_connection(self, opt=None):
        """
        Closes database cursor object for the instance

        Args:
            opt (_type_, optional): Defaults to None.

        Returns:
            None
        """
        self.db_conn.close()

    def fetch_query(self, opt):
        """
        Attempt to query SQLite database for data specified in input dictionary.
        Checks that all requested dates are returned from the database. Otherwise, returns False.

        Args:
            opt (dict): Dictionary of input parameters

        Returns:
            _type_: _description_
        """
        try:
            table_name = opt["from_curr"] + opt["to_curr"] + "_CHART"
            # check if table exists
            self.db_cursor.execute(
                f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}'"
            )
            table_exists = False
            for row in self.db_cursor.fetchall():
                if row[0] == 1:
                    table_exists = True
                    break
            if not table_exists:
                return False, None

            # check if all required dates exists in table
            data = pd.read_sql(
                sql=f'SELECT * FROM {table_name} WHERE Date BETWEEN \'{opt["start_date"]}\' AND \'{opt["end_date"]}\'',
                con=self.db_conn,
            )
            date_format = "%Y-%m-%d"
            # check dates in returned data
            date_set = set(data["Date"])
            for d in daterange(
                datetime.strptime(opt["start_date"], date_format),
                datetime.strptime(opt["end_date"], date_format),
            ):
                d = d.strftime(date_format)
                if d not in date_set:
                    return False, None
            # sort data on date field
            data = data.sort_values(by="Date", ignore_index=True)
            return True, data
        except sqlite3.Error as e:
            print(e)

    def save_query(self, opt: dict) -> None:
        """
        Attempts to save data into SQL table using an upsert method.
        Creates table if doesn't already exist.

        Args:
            opt (dict): Dictionary containing data
        """
        data = opt["data"]
        table_name = data.columns[1] + "_CHART"
        try:
            self.db_cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} ({data.columns[0]} TEXT, {data.columns[1]} REAL)"
            )
            self.db_conn.commit()
            # load existing table
            existing_df = pd.read_sql(
                sql=f"SELECT * FROM {table_name}", con=self.db_conn
            )
            # merge old data with new and drop duplicates
            data = pd.concat([data, existing_df], axis=0)
            data.drop_duplicates(subset=[data.columns[0]], inplace=True)
            # insert data into table
            data.to_sql(
                name=table_name, con=self.db_conn, index=False, if_exists="replace"
            )
        except sqlite3.Error as e:
            print(e)
