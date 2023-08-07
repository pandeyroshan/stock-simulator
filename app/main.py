import asyncio
import json

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from pydantic import BaseModel
from redis import asyncio as aioredis
from sqlalchemy import create_engine

from app.config import DATABASE_URL
from app.db.connection import Base
from app.router import consume, consume_stock_data, route
from app.routes.stock_data import stock_router
from app.routes.transaction import route as transaction_route
from app.routes.user import user_router

app = FastAPI(
    title="Stock Simulator",
    description="A simple stock simulator",
    version="0.1.0",
)


class Message(BaseModel):
    message : str


@app.get('/')
async def Home():
    """
    Home page
    """
    return "welcome home"



app.include_router(route)
app.include_router(prefix="/users", router=user_router)
app.include_router(prefix="/stocks", router=stock_router)
app.include_router(prefix="/transactions", router=transaction_route)



@app.on_event("startup")
async def startup_event():
    """
    This function will be executed only once when the application starts.
    """
    # Database connection
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    # Cache connection
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    # Kafka consumer
    # asyncio.create_task(consume())
    asyncio.create_task(consume_stock_data())
