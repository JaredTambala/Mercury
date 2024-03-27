from abc import ABC, abstractmethod

class DataFormatter(ABC):

    @staticmethod
    @abstractmethod
    def input_format(opt):
        pass

    @staticmethod
    @abstractmethod
    def output_format(opt):
        pass