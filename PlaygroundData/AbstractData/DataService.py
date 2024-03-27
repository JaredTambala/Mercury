from abc import ABC, abstractmethod

class DataService(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def save_data_to_store(self, data):
        pass

    @abstractmethod
    def format_data(self, data):
        pass
