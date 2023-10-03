# Ecommerece-admin-api


A FastAPI-based API for managing an e-commerce store's products, categories, sales, and inventory.

# Table of Contents
Introduction
Getting Started
Prerequisites
Installation
Configuration
Usage
API Endpoints
Demo Data
Contributing
License

# Introduction
This project provides a RESTful API built with FastAPI to manage an e-commerce store's operations, including product management, sales tracking, category management, and inventory control. It allows you to create, update, retrieve, and analyze product data, categories, and sales information.

# Getting Started
Follow these instructions to set up and run the project locally.

# Prerequisites
Before you begin, make sure you have the following prerequisites installed:

Python 3.7+
PostgreSQL (configured with appropriate credentials)
Required Python packages (install using pip install -r requirements.txt)

# Installation
Clone the project repository:

```bash
git clone <repository-url>
cd ecommerece-admin-api
```
Create a virtual environment (optional but recommended):

``` bash
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
```
# Install project dependencies:

```bash
pip install -r requirements.txt
```
# Set up the database configuration:

Copy the .env.example file to .env:

```bash
cp .env.example .env
Edit the .env file to configure your PostgreSQL database connection parameters, such as POSTGRESQL_HOST, POSTGRESQL_USER, POSTGRESQL_PASSWORD, and POSTGRESQL_DATABASE_NAME.
```

# Initialize the database:

```bash
python db.py
Start the API server:
```

```bash
python main.py
```

The API should now be running at http://localhost:8000 by default.

# Configuration
The project uses environment variables for configuration, which can be set in the .env file. Here are some important configuration options:

DEBUG: Set to 1 for debugging mode.
LOG_LEVEL: Logging level (default is INFO).
APP_HOST: Host for the API server (default is 0.0.0.0).
APP_PORT: Port for the API server (default is 8000).
URL_PREFIX: Prefix for API endpoints (e.g., /api/v1).
Usage
# API Documentation
You can access the API documentation using Swagger UI by visiting http://localhost:8000/docs in your browser.

# API Authentication
This API does not require authentication for the provided endpoints. Be cautious when deploying in a production environment.

# API Endpoints
# Categories
## Create Category
### Endpoint: POST /categories/create
Description: Creates a new product category.
Request Payload: Should include a JSON object with the category name.
Response: Returns the newly created category with its ID.
Example Request:
```json
{
  "name": "Electronics"
}
```

Example Response:
```json
{
  "category_id": 1,
  "category_name": "Electronics"
}
```

## Get Categories
### Endpoint: GET /categories
Description: Retrieves a list of all product categories.
Response: Returns a list of categories with their IDs and names.
Example Response:
```json
[
  {
    "category_id": 1,
    "category_name": "Electronics"
  },
  {
    "category_id": 2,
    "category_name": "Clothing"
  }
]
```
## Update Category
### Endpoint: PUT /categories/{category_id}
Description: Updates the name of a specific product category by ID.
Request Payload: Should include a JSON object with the new category name.
Response: Returns the updated category information.
Example Request:
```json
{
  "name": "Electronics and Gadgets"
}
```
Example Response:
```json
{
  "category_id": 1,
  "category_name": "Electronics and Gadgets"
}
```

# Products
## Create Product
### Endpoint: POST /products/create
Description: Creates a new product.
Request Payload: Should include a JSON object with product details such as name, description, price, inventory count, and category ID.
Response: Returns the newly created product with its ID.
Example Request:
```json
{
  "name": "Smartphone",
  "description": "High-end smartphone with advanced features.",
  "price": 699.99,
  "inventory_count": 50,
  "category_id": 1
}
```
Example Response:
```json
{
  "product_id": 1,
  "name": "Smartphone",
  "description": "High-end smartphone with advanced features.",
  "price": 699.99,
  "inventory_count": 50,
  "category_id": 1
}
```

## Get All Products
### Endpoint: GET /products
Description: Retrieves a list of all products.
Response: Returns a list of products with their IDs, names, and inventory counts.
Example Response:
```json
[
  {
    "product_id": 1,
    "product_name": "Smartphone",
    "inventory_count": 50
  },
  {
    "product_id": 2,
    "product_name": "Laptop",
    "inventory_count": 30
  }
]
```

## Get Single Product
### Endpoint: GET /products/{product_id}
Description: Retrieves a specific product by its ID.
Response: Returns the product details including name, description, price, inventory count, and category ID.
Example Response:
```json
{
  "product_id": 1,
  "name": "Smartphone",
  "description": "High-end smartphone with advanced features.",
  "price": 699.99,
  "inventory_count": 50,
  "category_id": 1
}
```
## Update Product
### Endpoint: PUT /products/{product_id}
Description: Updates the details of a specific product by its ID.
Request Payload: Should include a JSON object with the updated product details.
Response: Returns the updated product information.
Example Request:
```json
{
  "name": "New Smartphone Model",
  "price": 799.99
}
```

Example Response:
```json
{
  "product_id": 1,
  "name": "New Smartphone Model",
  "description": "High-end smartphone with advanced features.",
  "price": 799.99,
  "inventory_count": 50,
  "category_id": 1
}
```

## Get Inventory Status
### Endpoint: GET /inventory/status
Description: Retrieves the inventory status for all products, including a low stock alert.
Response: Returns a list of products with their IDs, names, inventory counts, and low stock alerts.
Example Response:
```json
[
  {
    "product_id": 1,
    "product_name": "Smartphone",
    "inventory_count": 50,
    "low_stock_alert": false
  },
  {
    "product_id": 2,
    "product_name": "Laptop",
    "inventory_count": 5,
    "low_stock_alert": true
  }
]
```

## Update Product Inventory
### Endpoint: PUT /inventory/update/{product_id}
Description: Updates the inventory count for a specific product by its ID.
Request Payload: Should include a JSON object with the quantity change (positive or negative) to update the inventory.
Response: Returns the updated product information.
Example Request:
``` json
{
  "quantity_change": -5
}
```

Example Response:
```json
{
  "product_id": 1,
  "name": "Smartphone",
  "inventory_count": 45,
  "category_id": 1
}
```

## Inventory Tracking History
### Endpoint: GET /inventory-history
Description: Retrieves the history of inventory changes, including product ID, inventory change amount, and date of change.
Response: Returns a list of inventory change records.
Example Response:
```json
[
  {
    "product_id": 1,
    "Inventory_change": -5,
    "Date_of_change": "2023-10-04 08:30:45.123456"
  },
  {
    "product_id": 2,
    "Inventory_change": 10,
    "Date_of_change": "2023-10-03 15:20:30.987654"
  }
]
```

# Sales
## Create Sale
### Endpoint: POST /sales/create
Description: Records a new sale, deducts the sold quantity from inventory, and calculates revenue.
Request Payload: Should include a JSON object with product ID and quantity sold.
Response: Returns the details of the newly created sale.
Example Request:
```json
{
  "product_id": 1,
  "quantity_sold": 3
}
```
Example Response:
```json
{
  "sale_id": 1,
  "product_id": 1,
  "sale_date": "2023-10-04 10:15:30.123456",
  "quantity_sold": 3
}
```

## Get Sales
### Endpoint: GET /sales
Description: Retrieves a list of all sales records within a specified date range and optional product/category filters.
Query Parameters: Start date, end date, product ID, and category ID.
Response: Returns a list of sales records with details.
Example Response:
```json
[
  {
    "sale_id": 1,
    "product_id": 1,
    "sale_date": "2023-10-04 10:15:30.123456",
    "quantity_sold": 3
  },
  {
    "sale_id": 2,
    "product_id": 2,
    "sale_date": "2023-10-04 11:20:45.987654",
    "quantity_sold": 2
  }
]
```

## Analyze Revenue
### Endpoint: GET /revenue/analysis
Description: Analyzes revenue within a specified date range, grouping by daily, weekly, monthly, or annual intervals.
Query Parameters: Start date, end date, and analysis interval.
Response: Returns revenue data grouped by the chosen interval.
Example Response:
```json
[
  {
    "interval": "2023-10-04",
    "revenue": 2000.0
  },
  {
    "interval": "2023-10-11",
    "revenue": 1500.0
  }
]
```

## Compare Revenue
### Endpoint: GET /revenue/comparison
Description: Compares revenue between two date ranges and an optional category filter.
Query Parameters: Start date and end date for two periods, and an optional category ID.
Response: Returns revenue data for both periods and the revenue difference.
Example Response:
```json
{
  "revenue_period_1": 2000.0,
  "revenue_period_2": 1500.0,
  "revenue_difference": 500.0
}
```

## Filter Sales
### Endpoint: GET /sales/filter
Description: Retrieves and filters sales data by date range, product, and category.
Query Parameters: Start date, end date, product ID, and category ID.
Response: Returns filtered sales data.
Example Response:
```json
[
  {
    "sale_id": 1,
    "product_id": 1,
    "sale_date": "2023-10-04 10:15:30.123456",
    "quantity_sold": 3
  },
  {
    "sale_id": 2,
    "product_id": 2,
    "sale_date": "2023-10-04 11:20:45.987654",
    "quantity_sold": 2
  }
]
```
These endpoints provide comprehensive functionality for managing categories, products, inventory, sales, and revenue analysis in your e-commerce API. You can use these endpoints to create, retrieve, update, and analyze data as needed for your application.




# Demo Data
You can populate the database with demo data for testing and development using the test.py script.

python test.py

# Contributing
Contributions are welcome! If you want to contribute to this project, please follow these steps:


Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes and commit them with clear, concise commit messages.
Push your branch to your fork.
Create a pull request to the main repository.


