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
    def conn_info(self) -> object:
        """
        Property for connection information - getter
        """

    @conn_info.setter
    @abstractmethod
    def conn_info(self, val: object) -> None:
        """
        Property for connection information - setter
        """

    @abstractmethod
    def open_connection(self, opt: object):
        """
        Function for creating a connection to the external data store
        """

    @abstractmethod
    def close_connection(self, opt: object) -> None:
        """
        Function for closing a connection to the external data store
        """

    @abstractmethod
    def fetch_query(self, opt: object) -> object:
        """
        Function for executing a data query - fetch
        """

    @abstractmethod
    def save_query(self, opt: object) -> None:
        """
        Function for executing a data query - save
        """
