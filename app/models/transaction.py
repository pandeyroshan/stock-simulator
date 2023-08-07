from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.db.connection import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    ticker = Column(String, index=True)
    transaction_type = Column(String)
    transaction_volume = Column(Integer)
    transaction_price = Column(Float)
    transaction_status = Column(String, default="PENDING")
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

def create_transaction(
    db: Session,
    user_id: int,
    ticker: str,
    transaction_type: str,
    transaction_volume: int,
    transaction_price: float,
) -> Transaction:
    new_transaction = Transaction(
        user_id=user_id,
        ticker=ticker,
        transaction_type=transaction_type,
        transaction_volume=transaction_volume,
        transaction_price=transaction_price,
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


# get transactions by user_id
def get_transactions_by_user_id(db: Session, user_id: int):
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()


# def get_transactions_by_filter(user_id: int, start_timestamp: str, end_timestamp: str,
def get_transactions_by_filter(db: Session, user_id: int, start_timestamp: str, end_timestamp: str):
    return db.query(Transaction).filter(Transaction.user_id == user_id).filter(Transaction.timestamp >= start_timestamp).filter(Transaction.timestamp <= end_timestamp).all()