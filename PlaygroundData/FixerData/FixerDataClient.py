import requests
import os
import json
from pathlib import Path
from dotenv import load_dotenv, dotenv_values
import datetime
from dateutil.relativedelta import relativedelta
from typing import *
from PlaygroundData.AbstractData import DataClient


class FixerDataClient(DataClient):
    """
    Client class for Fixer API
    """

    @property
    def auth_cred(self):
        return self._auth_cred

    @auth_cred.setter
    def auth_cred(self, val):
        self._auth_cred = val

    @property
    def conn_info(self):
        return self._conn_info

    @conn_info.setter
    def conn_info(self, val):
        self._conn_info = val

    def __init__(self):

        super().__init__()
        # load information from env file
        env_path = Path("test.env")
        load_dotenv(dotenv_path=env_path)
        self.conn_info = {"FIXER_API_URL": os.getenv("FIXER_API_URL")}
        self.auth_cred = {"FIXER_API_KEY": os.getenv("FIXER_API_KEY")}

    def request_data(self, opt):

        fixer_url = self.conn_info["FIXER_API_URL"] + "?"
        headers = {
            "apikey": self.auth_cred["FIXER_API_KEY"]
        }
        # calculate number of requests to send out and their parameters
        responses = []
        request_list = []
        start_date = opt["start_date"]
        end_date = opt["end_date"]
        s_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        e_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        diff_year = relativedelta(e_date, s_date).years
        if diff_year >= 10:
            raise ValueError("Maximum Date Range is 10 Years. Please Use Multiple Requests")
        delta_days = (e_date - s_date).days

        for i in range(0, (delta_days // 365) + 1):
            start = s_date + datetime.timedelta(days=max(0, i * 365))
            end = start + datetime.timedelta(days=365)
            if end >= e_date:
                end = e_date
            request_list.append((start, end))

        for params in request_list:
            fixer_url = self.conn_info["FIXER_API_URL"] + "?"
            s, e = params[0], params[1]
            arg_dict = {'start_date': s.strftime('%Y-%m-%d'),
                        'end_date': e.strftime('%Y-%m-%d'),
                        'base': opt["from_curr"],
                        'symbols': opt["to_curr"]
                        }
            for k, v in arg_dict.items():
                fixer_url += str(k) + "=" + str(v) + "&"
            fixer_url = fixer_url[:-1]
            response = requests.request(
                "GET",
                fixer_url,
                headers=headers,
            )
            responses.append(response.json())
        return responses
