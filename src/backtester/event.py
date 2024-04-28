"""
Module containing objects representing various kinds of of events
"""

import datetime
from abc import ABC

from symbols import SYMBOLS


class Event(ABC):
    """
    Abstract class for other events in dtrading infrastructure
    """


class MarketEvent(Event):
    """
    Represents the event of receiving a market update
    """

    def __init__(self):
        """
        Initialises the event
        """
        self.type = "MARKET"


class SignalEvent(Event):
    """
    Represents the event of sending a signal from a Strtategy to a Portfolio
    """

    def __init__(self, _symbol: str, _date: datetime.datetime, _signal_type: str):
        """
        Initialises the trading signal event

        Args:
            _symbol (str): Name of ticker symbol
            _date (datetime): Event time
            _signal_type (str): Type of signal
        """
        # type and value validation
        try:
            assert isinstance(_symbol, str) and _symbol in SYMBOLS
            assert isinstance(_date, datetime.datetime)
            assert isinstance(_signal_type, str) and _signal_type in ["LONG", "SHORT"]
        except AssertionError as e:
            raise TypeError(f"Bad initialisation. {str(e)}") from e
        self.type = "MARKET"
        self.symbol = _symbol
        self.date = _date
        self.signal_type = _signal_type


class OrderEvent(Event):
    """
    Represents the event of sending an order to be executed. Contains a symbol,
    type, quantity, direction.
    """

    def __init__(self, _symbol: str, _order_type: str, _quantity: int, _direction: str):
        """
        Intialises the order event.

        Args:
            _symbol (str): Name of ticker symbol
            _order_type (str): Order type. Can be Market order ('MKT')
            or Limit ('LMT') order
            quantity (int): order quantity, must be a non-negative integer
            direction (str): 'BUY' or 'SELL' for long or short
        """
        # type and value validation
        try:
            assert isinstance(_symbol, str) and _symbol in SYMBOLS
            assert isinstance(_order_type, str) and _order_type in ["MKT", "LMT"]
            assert isinstance(_quantity, int) and _quantity >= 0
            assert isinstance(_direction, str) and _direction in ["BUY", "SELL"]
        except AssertionError as e:
            raise TypeError(f"Bad initialisation. {str(e)}") from e

        self.type = "ORDER"
        self.symbol = _symbol
        self.order_type = _order_type
        self.quantity = _quantity
        self.direction = _direction

    def __str__(self):
        """
        Creates string representation of the order
        """
        try:
            order_repr = (
                f"Symbol: {self.symbol}, Type: {self.order_type}, "
                + f"Quantity: {self.quantity}, Direction: {self.direction}"
            )
            return order_repr
        except Exception as e:
            raise RuntimeError(
                f"Could not generate string representation of order. {str(e)}"
            ) from e
