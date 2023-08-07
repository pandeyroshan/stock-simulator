import asyncio

# env Variable
KAFKA_BOOTSTRAP_SERVERS= "kafka:9092"
DATABASE_URL="postgresql://stock_simulator:password@db:5432/stock_simulator"
KAFKA_TOPIC="kafka"
STOCK_TOPIC="stock_data"
KAFKA_CONSUMER_GROUP="group-id"
loop = asyncio.get_event_loop()
redis_url = "redis://redis:6379"
