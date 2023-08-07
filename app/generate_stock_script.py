import asyncio
import json
import random
import time
from datetime import datetime

from aiokafka import AIOKafkaProducer
from pydantic import BaseModel

KAFKA_BOOTSTRAP_SERVERS= "localhost:9093"
STOCK_TOPIC="stock_data"


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

# Sample list of top 50 US tickers
TOP_50_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB", "BRK.B", "JPM", "JNJ", "V", "WMT",
                  "PG", "UNH", "DIS", "NVDA", "HD", "KO", "MRK", "INTC", "VZ", "PFE",
                  "BA", "CSCO", "XOM", "CRM", "ADBE", "CMCSA", "PEP", "T", "NFLX", "MCD",
                  "ABT", "ACN", "COST", "CVX", "MDT", "PYPL", "PM", "LLY", "BAC", "NEE",
                  "TMO", "UNP", "DHR", "TXN", "AMGN", "IBM", "AVGO", "QCOM", "LIN", "GS"]

async def generate_random_stock_data():
    """
    To generate random stock data and send it to the Kafka topic.
    """
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        for ticker in TOP_50_TICKERS:
            print(f'Sending stock to kafka: {ticker}')
            time.sleep(1)
            open_price = random.uniform(50, 1500)
            close_price = open_price + random.uniform(-10, 10)
            high = max(open_price, close_price) + random.uniform(0, 5)
            low = min(open_price, close_price) - random.uniform(0, 5)
            current_price = random.uniform(low, high)
            volume = random.randint(1000, 1000000)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            stock = StockCreate(
                ticker=ticker, open_price=open_price, close_price=close_price,
                current_price=current_price, high=high, low=low, volume=volume, timestamp=timestamp
            )
            value_json = json.dumps(stock.model_dump()).encode('utf-8')
            await producer.send_and_wait(STOCK_TOPIC, value=value_json)
    finally:
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(generate_random_stock_data())