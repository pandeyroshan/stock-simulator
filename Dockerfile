# Use an official Python runtime as a base image
FROM python:3.11.2-slim-buster

# Set environment variables
# Ensure that Python outputs everything that's printed inside the application (unbuffered mode)
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    netcat \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installing requirements
COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY wait_for_postgres.sh /wait_for_postgres.sh
COPY wait_for_kafka.sh /wait_for_kafka.sh

RUN chmod +x /wait_for_postgres.sh /wait_for_kafka.sh

# Copying actuall application
COPY . /app