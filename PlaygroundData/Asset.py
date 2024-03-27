import datetime
from abc import ABC
from dataclasses import dataclass


@dataclass
class Asset:
    date: datetime.datetime
    open: float
    close: float
    high: float
    low: float


@dataclass
class ForexAsset:
    currency_from: str
    currency_to: str


@dataclass
class AssetGroup:
    type: str
    assets: list[Asset]
