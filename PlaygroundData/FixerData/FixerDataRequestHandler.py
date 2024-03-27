import datetime
from typing import *

from .FixerDataClient import FixerDataClient
from .FixerDataService import FixerDataService
from .FixerDataStoreHandler import FixerDataStoreHandler
from PlaygroundData.AbstractData import DataRequestHandler


class FixerDataRequestHandler(DataRequestHandler):

    from_curr = None
    to_curr = None

    def __init__(self):
        super().__init__()

    @property
    def start_date(self):
        return self.sd

    @start_date.setter
    def start_date(self, val):
        self.sd = val

    @property
    def end_date(self):
        return self.ed

    @end_date.setter
    def end_date(self, val):
        self.ed = val

    @property
    def asset_type(self):
        return self.at

    @asset_type.setter
    def asset_type(self, val):
        self.at = val

    def get_data(self, opt_dict):

        # validate input
        valid, message = self.input_validation(opt_dict)
        if not valid:
            raise ValueError(message)
        # set properties
        self.start_date = opt_dict["start_date"]
        self.end_date = opt_dict["end_date"]
        self.asset_type = opt_dict["from_curr"].upper() + opt_dict["to_curr"].upper()
        self.from_curr = opt_dict["from_curr"]
        self.to_curr = opt_dict["to_curr"]
        # attempt to directly load data from persistent store
        opt_dict = {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "from_curr": self.from_curr,
            "to_curr": self.to_curr
        }
        fdsh = FixerDataStoreHandler()
        fds = FixerDataService()
        fdsh.open_connection()
        data = None
        print("Attempting to fetch data from SQL database.")
        data_exists, data = fdsh.fetch_query(opt_dict)
        # if data does not exist in persistent store, get from online and persist
        if not data_exists:
            print("Data does not yet exist in SQL Database. Attempt to fetch from Fixer API...")
            fdc = FixerDataClient()
            data_list = fdc.request_data(opt_dict)
            print("Done.")
            print("Formatting.")
            f_data_list = []
            for data in data_list:
                f_data = fds.format_data(data)
                f_data_list.append(f_data)
            print("Saving to SQL Database.")
            for f_data in f_data_list:
                fds.save_data_to_store(f_data)
            print("Save complete.")
            data_exists, data = fdsh.fetch_query(opt_dict)
        fdsh.close_connection()
        return data


    def input_validation(self, opt_dict):

        input_keys = opt_dict.keys()
        if set(input_keys) != {"start_date", "end_date", "from_curr", "to_curr"}:
            return False, "Parameter list incomplete"
        sd = opt_dict["start_date"]
        ed = opt_dict["end_date"]
        fc = opt_dict["from_curr"]
        tc = opt_dict["to_curr"]

        if any(map(lambda x: type(x) != str, [sd, ed, fc, tc])):
            return False, "All parameters must be type str"
        s_date = None
        e_date = None
        try:
            s_date = datetime.datetime.strptime(sd, '%Y-%m-%d')
            e_date = datetime.datetime.strptime(ed, '%Y-%m-%d')
        except ValueError:
            return False, "Incorrect date format, use YYYY-MM-DD"
        if len(fc) != 3:
            return False, "From Currency is Invalid"
        if len(tc) != 3:
            return False, "To Currency is Invalid"

        days_between = (e_date - s_date).days
        if days_between < 0:
            return False, "End Date Is Before Start Date"

        return True, ""

    def handle_error(self):
        pass

