"""
Implementation of Data Formatter for Fixer API
"""

import pandas as pd

from playground_data.abstract_data import DataFormatter


class FixerDataFormatter(DataFormatter):
    """
    Class definition
    """

    @staticmethod
    def input_format(opt: dict) -> pd.DataFrame:
        """
        Formats dat received directly from the Fixer Data API into a flat structure
        which can be ingested by a persistent data store

        Args:
            opt (dict): Dictionary containing data from Fixer API

        Returns:
            pd.DataFrame: Pandas DataFrame containing flattened data
        """
        json_data = opt["data"]
        # get base curr
        base_curr = json_data["base"]
        # get to curr
        to_curr = list(json_data["rates"][list(json_data["rates"].keys())[0]].keys())[0]
        # loop through rates and add each key-value to lists
        curr_pair = f"{base_curr}{to_curr}"
        format_dict = {"Date": [], curr_pair: []}
        for date, rate_dict in json_data["rates"].items():
            format_dict["Date"].append(date)
            rate = list(rate_dict.values())[0]
            format_dict[curr_pair].append(rate)

        format_df = pd.DataFrame(format_dict)
        return format_df
