"""
Defines an interface for interacting with persistent data storage
"""

from abc import ABC, abstractmethod


class DataStoreHandler(ABC):
    """
    Abstract class for handling data storage sources
    """

    def __init__(self):
        """
        No initialiser
        """

    @property
    @abstractmethod
    def conn_info(self):
        """
        Property for connection information - getter
        """

    @conn_info.setter
    @abstractmethod
    def conn_info(self, val) -> None:
        """
        Property for connection information - setter
        """

    @abstractmethod
    def open_connection(self, opt):
        """
        Function for creating a connection to the external data store
        """

    @abstractmethod
    def close_connection(self, opt) -> None:
        """
        Function for closing a connection to the external data store
        """

    @abstractmethod
    def fetch_query(self, opt):
        """
        Function for executing a data query - fetch
        """

    @abstractmethod
    def save_query(self, opt) -> None:
        """
        Function for executing a data query - save
        """
