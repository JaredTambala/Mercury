"""
Implements the Data Service for Fixer Data API
"""

from pandas import DataFrame

from playground_data.abstract_data import DataService

from .fixer_data_formatter import FixerDataFormatter
from .fixer_data_store_handler import FixerDataStoreHandler


class FixerDataService(DataService):
    """
    Class definition
    """

    def __init__(self):
        pass

    def save_data_to_store(self, data: DataFrame) -> None:
        """
        Attempts to save data to peristent data storage

        Args:
            data (DataFrame): Pandas Dataframe containing data from Fixer API

        Returns:
            None
        """
        fdsh = FixerDataStoreHandler()
        fdsh.open_connection()
        fdsh.save_query({"data": data})
        fdsh.close_connection()

    def format_data(self, data: dict) -> DataFrame:
        """
        Formats data directly fetched from Fixer API into a Pandas
        Dataframe

        Args:
            data (dict): Dinctionary object containing raw data

        Returns:
            DataFrame: Pandas DataFrame containing deata from Fixer API
        """
        format_df = FixerDataFormatter.input_format({"data": data})
        return format_df
