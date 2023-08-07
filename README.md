# Stock Simulator API

Welcome to the **Stock Simulator API** documentation. This API provides endpoints to simulate stock trading and manage user transactions. It's designed to help you create, retrieve, and manage user accounts, stock data, and transactions for a simple stock trading simulation.

## Steps to run
1. Bash script for project setup 
```
./start.sh
```
2. Visit the [API Doc here](http://localhost:8000/docs#/) to try out the APIs
## Table of Contents

- [Introduction](#introduction)
- [Endpoints](#endpoints)
  - [Home](#home)
  - [Create User Account](#create-user-account)
  - [Get User Account](#get-user-account)
  - [Get Stocks](#get-stocks)
  - [Ingest Stock Data](#ingest-stock-data)
  - [Get Stock](#get-stock)
  - [Create Transaction](#create-transaction)
  - [Get Transactions](#get-transactions)
  - [Get Transactions By Filter](#get-transactions-by-filter)
- [Components](#components)
  - [Schemas](#schemas)
    - [HTTPValidationError](#httpvalidationerror)
    - [Message](#message)
    - [StockCreate](#stockcreate)
    - [TransactionCreate](#transactioncreate)
    - [UserCreate](#usercreate)
    - [ValidationError](#validationerror)

## Introduction

The **Stock Simulator** API is a RESTful service built using OpenAPI 3.1.0. It provides functionality to create user accounts, retrieve user details, fetch stock data, manage stock data ingestion, create transactions, and retrieve transaction history. The API is designed to be simple to use and integrate into your stock trading simulation application.

## Endpoints

### Home

- **Method:** GET
- **Path:** `/`
- **Summary:** Home
- **Description:** Home page
- **Response:**
  - Status Code: 200
  - Content Type: application/json
  - Schema: Empty

### Create User Account

- **Method:** POST
- **Path:** `/users/register`
- **Summary:** Create User Account
- **Description:** Create a new user account
- **Request Body:**
  - Content Type: application/json
  - Schema: [UserCreate](#usercreate)
- **Response:**
  - Status Code: 200
  - Content Type: application/json
  - Schema: Empty

<!-- Rest of the endpoints follow the same format... -->

### Get Transactions By Filter

- **Method:** GET
- **Path:** `/transactions/{user_id}/{start_timestamp}/{end_timestamp}`
- **Summary:** Get Transactions By Filter
- **Parameters:**
  - `user_id` (path parameter): User's ID
  - `start_timestamp` (path parameter): Start timestamp for filtering transactions
  - `end_timestamp` (path parameter): End timestamp for filtering transactions
- **Response:**
  - Status Code: 200
  - Content Type: application/json
  - Schema: Empty

## Components

### Schemas

#### HTTPValidationError

- **Type:** object
- **Properties:**
  - `detail` (array of [ValidationError](#validationerror)): Validation error details

#### Message

- **Type:** object
- **Properties:**
  - `message` (string): Message content

#### StockCreate

- **Type:** object
- **Properties:**
  - `ticker` (string): Ticker symbol
  - `open_price` (number): Opening price
  - `close_price` (number): Closing price
  - `current_price` (number): Current price
  - `high` (number): High price
  - `low` (number): Low price
  - `volume` (integer): Volume
  - `timestamp` (string): Timestamp of stock data

#### TransactionCreate

- **Type:** object
- **Properties:**
  - `user_id` (integer): User's ID
  - `ticker` (string): Ticker symbol
  - `transaction_type` (string): Transaction type
  - `transaction_volume` (integer): Transaction volume

#### UserCreate

- **Type:** object
- **Properties:**
  - `username` (string): Username
  - `initial_balance` (number): Initial balance

#### ValidationError

- **Type:** object
- **Properties:**
  - `loc` (array of anyOf[string, integer]): Location of the error
  - `msg` (string): Error message
  - `type` (string): Error type

Feel free to explore the endpoints and schemas to understand how to interact with the Stock Simulator API.
