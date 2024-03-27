"""
Defines interfaces for service functions
"""

from abc import ABC, abstractmethod


class DataService(ABC):
    """
    Abstract class for service functions
    """

    def __init__(self):
        """
        No abstract initialiser
        """

    @abstractmethod
    def save_data_to_store(self, data: object) -> None:
        """
        Function for saving data to external data storage
        """

    @abstractmethod
    def format_data(self, data: object) -> object:
        """
        Function for formatting data
        """
