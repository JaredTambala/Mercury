from abc import ABC, abstractmethod

class DataClient(ABC):

    def __init__(self):
        pass

    @property
    @abstractmethod
    def auth_cred(self):
        pass

    @auth_cred.setter
    @abstractmethod
    def auth_cred(self, val):
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
    def request_data(self, opt):
        pass
