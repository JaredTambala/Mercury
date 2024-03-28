# pylint: disable=W0221,E1121,E1120
"""
Defines an interface for connecting and fetching data from external data stores
"""

from abc import ABC, abstractmethod

import requests


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
    def auth_cred(self, **kwargs) -> None:
        """
        Property for authentication credentials - setter
        """

    @property
    @abstractmethod
    def conn_info(self):
        """
        Property for connection information - getter
        """

    @conn_info.setter
    @abstractmethod
    def conn_info(self, **kwargs) -> None:
        """
        Property for connection information - getter
        """

    @abstractmethod
    def request_data(self, **kwargs):
        """
        Function for requesting data from external souce
        """

    @abstractmethod
    def build_request(self, **kwargs):
        """
        Function for building request parameters
        """


class RestApiDataClient(DataClient):
    """
    Implementation for requesting data from REST API sources. Uses the standard
    requests library.
    """

    def __init__(self):
        pass

    @property
    def request_header(self) -> dict:
        """
        Returns request header
        """
        return self._request_header

    @request_header.setter
    def request_header(self, val: dict) -> None:
        """
        Property representing dictionary containing request headers.
        These will be used for sending requests
        """
        self._request_header = val

    def request_data(self, method, url, _timeout):
        """
        Used for requesting data from a REST API. Returns response as JSON
        dictionary

        Args:
            method (str): HTTP method.
            url (str): Request URL
            timeout (int): Request timeout (seconds)

        Returns:
            dict: JSON response
        """
        response = requests.request(method, url, self.request_header, timeout=_timeout)
        return response.json()

    def build_request(self, base_url, query_dict):
        """
        Builds a full URL string with query from a base url and a key-value dictionary. For example,
        given a url "http://www.mysite.com" and a query dictionary {"name": Jacob, "age": 34}, the
        function will return a URL "http://www.mysite.com?name=Jacob&age=34"

        Args:
            base_url (str): Base URL
            query_dict (dict): Dictionary of query values

        Returns:
            str: Full URL including query parameters
        """

        full_url = (
            base_url
            + "?"
            + "".join(
                [
                    str(key_name) + "=" + str(key_val) + "&"
                    for key_name, key_val in query_dict.items()
                ]
            )[:-1]
        )
        return full_url
