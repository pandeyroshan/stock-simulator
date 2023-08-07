#!/bin/bash

# Ensure script stops on first error
set -e

# Start docker-compose services
echo "Starting services from docker-compose.yml..."
docker-compose up --build --detach
echo "Services from docker-compose.yml started."

# Wait for 30 seconds for kafka to ready
echo "Waiting for 30 seconds for kafka to ready..."
sleep 30

# Start the fastapi container
echo "Starting fastapi container..."
docker-compose restart fastapi

docker exec -it fastapi python /app/generate_stock_script.py

# End of script
echo "Script finished."
