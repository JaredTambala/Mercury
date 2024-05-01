# pylint: disable=R0902
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


class FillEvent(Event):
    """
    Represents a filled order returned from a brokerage. Stores the quantity
    and price of the asset. Stores the brokerage commission from the trade
    """

    def __init__(
        self,
        _time_index: str,
        _symbol: str,
        _exchange: str,
        _quantity: int,
        _direction: str,
        _fill_cost: int,
        _commission: int,
    ):
        """
        Initialises the object.

        Args:
            _time_index (str): Bar resolution when order was filled
            _symbol (str): Instrument which was filled
            _exchange (str): Exchange where the order was filled
            _quantity (int): Filled quantity
            _direction (str): Direction of fill
            _fill_cost (int): Holding value
            _commission (Union[int, None]): Commission (optional)
        """
        # type validation
        try:
            assert isinstance(_time_index, str)
            assert isinstance(_symbol, str)
            assert isinstance(_exchange, str)
            assert isinstance(_quantity, int)
            assert isinstance(_direction, str)
            assert isinstance(_fill_cost, int)
            assert isinstance(_commission, int)
        except AssertionError as e:
            raise TypeError(f"Bad initialisation. {str(e)}") from e
        self.type = "FILL"
        self.time_index = _time_index
        self.symbol = _symbol
        self.exchange = _exchange
        self.quantity = _quantity
        self.direction = _direction
        self.fill_cost = _fill_cost
        self.commission = _commission
