from datetime import datetime
from sqlite3 import Date

from pydantic import BaseModel


class StockCreate(BaseModel):
    """
    StockCreate is a class that describes the request body for creating a new stock.
    """
    ticker: str
    open_price: float
    close_price: float
    current_price: float
    high: float
    low: float
    volume: int
    timestamp: str