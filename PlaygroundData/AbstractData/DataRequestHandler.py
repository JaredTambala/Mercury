from abc import ABC, abstractmethod


class DataRequestHandler(ABC):

    def __init__(self):
        pass

    @property
    @abstractmethod
    def start_date(self):
        pass

    @start_date.setter
    @abstractmethod
    def start_date(self, val):
        pass

    @property
    @abstractmethod
    def end_date(self):
        pass

    @end_date.setter
    @abstractmethod
    def end_date(self, val):
        pass

    @property
    @abstractmethod
    def asset_type(self):
        pass

    @asset_type.setter
    @abstractmethod
    def asset_type(self, val):
        pass

    @abstractmethod
    def get_data(self, opt_dict):
        pass

    @abstractmethod
    def input_validation(self, opt_dict):
        pass

    @abstractmethod
    def handle_error(self):
        pass
