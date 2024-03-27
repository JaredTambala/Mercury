"""
Defines an interface for formatting data
"""

from abc import ABC, abstractmethod


class DataFormatter(ABC):
    """
    Abstract class for data formatters
    """

    @staticmethod
    @abstractmethod
    def input_format(opt):
        """
        Formatting function for data ingested from external API
        """

    @staticmethod
    @abstractmethod
    def output_format(opt):
        """
        Formatting function for data fetched from persistent store
        """
