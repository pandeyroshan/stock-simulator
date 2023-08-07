#!/bin/sh
# wait_for_kafka.sh
set -e

KAFKA_HOST=kafka
KAFKA_PORT=9093

cmd="$@"
until echo > /dev/tcp/$KAFKA_HOST/$KAFKA_PORT; do
  >&2 echo "Kafka is unavailable - sleeping"
  sleep 1
done
>&2 echo "Kafka is up - executing command"
exec $cmd
