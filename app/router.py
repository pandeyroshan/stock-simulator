import asyncio
import json
from math import e

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import APIRouter
from pydantic import BaseModel

from .config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_CONSUMER_GROUP,
    KAFKA_TOPIC,
    STOCK_TOPIC,
    loop,
)
from .db.connection import SessionLocal
from .models.stock_data import create_stock, get_all_stocks
from .schema.stock import StockCreate
from .utils.redis import set_cache


class Message(BaseModel):
    message: str

route = APIRouter()

@route.post('/create_message')
async def send(message: Message):
    producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        print(f'Sendding message with value: {message}')
        value_json = json.dumps(message.__dict__).encode('utf-8')
        await producer.send_and_wait(topic=KAFKA_TOPIC, value=value_json)
    finally:
        await producer.stop()


async def consume():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id=KAFKA_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            print(f'Consumer msg: {msg}')
    finally:
        await consumer.stop()

async def consume_stock_data():
    db = SessionLocal()
    consumer = AIOKafkaConsumer(
        STOCK_TOPIC, loop=loop,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_CONSUMER_GROUP
    )
    await consumer.start()
    try:
        async for msg in consumer:
            if msg.value is not None:
                stock = json.loads(msg.value)
                print(f'Consumer msg: {stock}')
                data = StockCreate(**stock)

                # create stock in the database
                stock_created_in_db = create_stock(db, data)

                # Get all stocks from the database
                all_stock = get_all_stocks(db)
                all_stock_map = map(lambda x: x.as_dict(), all_stock)
                all_stock_json = json.dumps(list(all_stock_map))

                # set stock to the redis cache for all_stocks
                set_cache("all_stocks", all_stock_json)

                # Set stock to the redis cache for stock ticker
                set_cache(str(stock_created_in_db.ticker), json.dumps(stock_created_in_db.as_dict()))
    except Exception as e:
        # sleep for 10 seconds if there is an error and then restart the consumer (only 5 retries)
        for _ in range(5):
            await asyncio.sleep(10)
            print(f"Error: {e}. Restarting consumer")
            await consumer.start()

    finally:
        await consumer.stop()
