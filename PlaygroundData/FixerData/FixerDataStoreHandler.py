from typing import *
import sqlite3
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv, dotenv_values
from datetime import timedelta, date, datetime
from PlaygroundData.AbstractData import DataStoreHandler


def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)


class FixerDataStoreHandler(DataStoreHandler):

    def __init__(self):
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

    def open_connection(self, opt=None):

        try:
            db_conn = sqlite3.connect(self.conn_info.get("DB_FILE"))
            self.db_conn = db_conn
            self.db_cursor = self.db_conn.cursor()
        except sqlite3.Error as e:
            print(e)
            if self.db_conn:
                self.close_connection()

    def close_connection(self, opt=None):
        self.db_conn.close()
        return

    def fetch_query(self, opt):

        try:
            table_name = opt["from_curr"] + opt["to_curr"] + "_CHART"
            # check if table exists
            self.db_cursor.execute(
                f'SELECT count(*) FROM sqlite_master WHERE type=\'table\' AND name=\'{table_name}\''
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
                con=self.db_conn
            )
            date_format = '%Y-%m-%d'
            # check dates in returned data
            date_set = set(data["Date"])
            for d in daterange(datetime.strptime(opt["start_date"], date_format),
                                datetime.strptime(opt["end_date"], date_format)):
                d = d.strftime(date_format)
                if d not in date_set:
                    return False, None
            # sort data on date field
            data = data.sort_values(by="Date", ignore_index=True)
            return True, data
        except sqlite3.Error as e:
            print(e)


    def save_query(self, opt):
        data = opt["data"]
        table_name = data.columns[1] + "_CHART"
        try:
            self.db_cursor.execute(
                f'CREATE TABLE IF NOT EXISTS {table_name} ({data.columns[0]} TEXT, {data.columns[1]} REAL)'
            )
            self.db_conn.commit()
            # load existing table
            existing_df = pd.read_sql(
                sql=f'SELECT * FROM {table_name}',
                con=self.db_conn
            )
            # merge old data with new and drop duplicates
            data = pd.concat([data, existing_df], axis=0)
            data.drop_duplicates(subset=[data.columns[0]], inplace=True)
            # insert data into table
            data.to_sql(
                name=table_name,
                con=self.db_conn,
                index=False,
                if_exists='replace'
            )
        except sqlite3.Error as e:
            print(e)

