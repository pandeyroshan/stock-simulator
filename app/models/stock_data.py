from re import S

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import Session

from app.db.connection import Base
from app.schema.stock import StockCreate


class StockData(Base):
    __tablename__ = 'stock_data'

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    open_price = Column(Float)
    close_price = Column(Float)
    current_price = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)
    timestamp = Column(String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def get_all_stocks(db: Session):
    """
    Get all stocks from the database
    """
    return db.query(StockData).all()

def get_stock_by_ticker(db: Session, ticker):
    """
    Get a stock by ticker from the database
    """
    return db.query(StockData).filter(StockData.ticker == ticker).first()

def create_stock(db: Session, data: StockCreate):
    """
    Create a new stock to the database
    """
    new_stock = StockData(
        ticker=data.ticker,
        open_price=data.open_price,
        close_price=data.close_price,
        current_price=data.current_price,
        high=data.high,
        low=data.low,
        volume=data.volume,
        timestamp=data.timestamp
    )
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return new_stock
