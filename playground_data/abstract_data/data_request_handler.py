"""
Defines an interface for fetching Time Series data from external sources
"""

from abc import ABC, abstractmethod


class DataRequestHandler(ABC):
    """
    Abstract class for data request handling
    """

    def __init__(self):
        """
        No initialiser specified
        """

    @property
    @abstractmethod
    def start_date(self) -> object:
        """
        Property for start date - getter
        """

    @start_date.setter
    @abstractmethod
    def start_date(self, val: object) -> None:
        """
        Property for start date - setter
        """

    @property
    @abstractmethod
    def end_date(self) -> object:
        """
        Property for end date - getter
        """

    @end_date.setter
    @abstractmethod
    def end_date(self, val: object) -> None:
        """
        Property for end date - setter
        """

    @property
    @abstractmethod
    def asset_type(self) -> object:
        """
        Property for asset type - getter
        """

    @asset_type.setter
    @abstractmethod
    def asset_type(self, val: object) -> None:
        """
        Property for asset type - setter
        """

    @abstractmethod
    def get_data(self, opt_dict: object) -> object:
        """
        Function for requesting data from external source
        """

    @abstractmethod
    def input_validation(self, opt_dict: object) -> bool:
        """
        Function for validating input
        """
