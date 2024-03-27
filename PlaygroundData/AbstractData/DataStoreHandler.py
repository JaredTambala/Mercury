from abc import ABC, abstractmethod

class DataStoreHandler:

    def __init__(self):
        pass

    @property
    @abstractmethod
    def conn_info(self):
        pass

    @conn_info.setter
    @abstractmethod
    def conn_info(self, val):
        pass

    @abstractmethod
    def open_connection(self, opt):
        pass

    @abstractmethod
    def close_connection(self, opt):
        pass

    @abstractmethod
    def fetch_query(self, opt):
        pass

    @abstractmethod
    def save_query(self, opt):
        pass


