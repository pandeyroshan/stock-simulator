from enum import Enum

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session

from app.db.connection import SessionLocal, get_db
from app.models.stock_data import get_stock_by_ticker
from app.models.transaction import create_transaction, get_transactions_by_user_id
from app.models.user import get_user, get_user_by_id
from app.worker import celery

route = APIRouter()

class TransactionCreate(BaseModel):
    user_id: int
    ticker: str
    transaction_type: str
    transaction_volume: int


# POST /transactions/: To post a new transaction.
# This should take user_id, ticker, transaction_type, and transaction_volume as inputs.
# The endpoint should calculate the transaction_price based on the current stock price and update the user's balance.
@route.post('')
async def create(transaction: TransactionCreate, db: Session = Depends(get_db)):
    celery.send_task('process_transaction', args=[transaction, db])

# . Redis and Celery Task Queue:
# a. When a new transaction is posted, FastAPI should send a task to Celery via Redis for processing. The task queue should be designed to scale to handle high volumes of transactions.
@celery.task(name='process_transaction')
def process_transaction(transaction: TransactionCreate, db: Session):
    # Data Processing:
    # a. The processing should validate the transaction (e.g., check if the user has enough balance for a buy transaction) and update the Users and Transactions tables accordingly.
    try:
        user = get_user_by_id(db, transaction.user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        stock = get_stock_by_ticker(db, transaction.ticker)
        if stock is None:
            raise HTTPException(status_code=404, detail="Stock not found")
        if transaction.transaction_type == 'BUY':
            if user.balance < stock.current_price * transaction.transaction_volume:
                raise HTTPException(status_code=400, detail="Insufficient balance")
            user.balance -= stock.current_price * transaction.transaction_volume
        elif transaction.transaction_type == 'SELL':
            if user.balance < stock.current_price * transaction.transaction_volume:
                raise HTTPException(status_code=400, detail="Insufficient balance")
            user.balance += stock.current_price * transaction.transaction_volume
        else:
            raise HTTPException(status_code=400, detail="Invalid transaction type")
        db.commit()
        db.refresh(user)
        transaction = create_transaction(
            db,
            user_id=transaction.user_id,
            ticker=transaction.ticker,
            transaction_type=transaction.transaction_type,
            transaction_volume=transaction.transaction_volume,
            transaction_price=stock.current_price,
        )
        # Send task to Celery
        celery.send_task('process_transaction', args=[transaction])

        return transaction
    except ValidationError as e:
        return JSONResponse(status_code=400, content=e.errors())
    finally:
        db.close()


# GET /transactions/{user_id}/: To retrieve all transactions of a specific user.
@route.get('/{user_id}')
async def get_transactions(user_id: int, db: Session = Depends(get_db)):
    return get_transactions_by_user_id(db, user_id)

# GET /transactions/{user_id}/{start_timestamp}/{end_timestamp}/: To retrieve transactions of a specific user between two timestamps.
@route.get('/{user_id}/{start_timestamp}/{end_timestamp}')
async def get_transactions_by_filter(user_id: int, start_timestamp: str, end_timestamp: str, db: Session = Depends(get_db)):
    return get_transactions_by_user_id(db, user_id)
