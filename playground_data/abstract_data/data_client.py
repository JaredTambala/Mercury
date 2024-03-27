"""
Defines an interface for connecting and fetching data from external data stores
"""

from abc import ABC, abstractmethod


class DataClient(ABC):

    """
    Interface for Data Clients
    """

    def __init__(self):
        """
        No initialiser
        """

    @property
    @abstractmethod
    def auth_cred(self) -> object:
        """
        Property for authentication credentials - getter
        """

    @auth_cred.setter
    @abstractmethod
    def auth_cred(self, val) -> None:
        """
        Property for authentication credentials - setter
        """

    @property
    @abstractmethod
    def conn_info(self) -> object:
        """
        Property for connection information - getter
        """

    @conn_info.setter
    @abstractmethod
    def conn_info(self, val) -> None:
        """
        Property for connection information - getter
        """

    @abstractmethod
    def request_data(self, opt):
        """
        Function for requesting data from external souce
        """
