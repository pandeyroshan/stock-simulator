import asyncio
import json

from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import KAFKA_BOOTSTRAP_SERVERS, STOCK_TOPIC
from app.db.connection import SessionLocal, get_db
from app.models.stock_data import create_stock, get_all_stocks, get_stock_by_ticker
from app.schema.stock import StockCreate

from ..utils.redis import get_cache

stock_router = APIRouter()


@stock_router.post("")
async def ingest_stock_data(stock: StockCreate):
    """
    To ingest stock data from the Kafka topic and store it in the Postgres database.
    """
    loop = asyncio.get_event_loop()

    producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        print(f'Sending in kafka: {stock}')
        value_json = json.dumps(stock.__dict__).encode('utf-8')
        await producer.send_and_wait(topic=STOCK_TOPIC, value=value_json)
    finally:
        await producer.stop()



# GET /stocks/:
# To get all the stocks from the database.
@stock_router.get("")
async def get_stocks(db: Session = Depends(get_db)):
    """
    To retrieve all stock data. Use Redis to cache stock data and fetch it from the cache when available.
    """
    if stock_from_cache := get_cache("all_stocks"):
        print("Stocks retrieved from cache")
        return stock_from_cache
    return get_all_stocks(db)


# GET /stocks/{ticker}/:
# To retrieve specific stock data. Use Redis to cache this data and fetch it from the cache when available.
@stock_router.get("/{ticker}")
async def get_stock(ticker: str, db: Session = Depends(get_db)):
    """
    To retrieve specific stock data. Use Redis to cache this data and fetch it from the cache when available.
    """
    if stock_from_cache := get_cache(ticker):
        print("Stock retrieved from cache")
        return stock_from_cache
    return get_stock_by_ticker(db, ticker)