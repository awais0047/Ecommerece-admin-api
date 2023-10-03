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

bash
Copy code
git clone <repository-url>
cd ecommerece-admin-api
Create a virtual environment (optional but recommended):

bash
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
Install project dependencies:

bash
pip install -r requirements.txt
Set up the database configuration:

Copy the .env.example file to .env:

bash
cp .env.example .env
Edit the .env file to configure your PostgreSQL database connection parameters, such as POSTGRESQL_HOST, POSTGRESQL_USER, POSTGRESQL_PASSWORD, and POSTGRESQL_DATABASE_NAME.

Initialize the database:

bash
python db.py
Start the API server:

bash
python main.py
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
# Products
POST /products/create: Create a new product.
GET /products/: Retrieve a list of all products.
GET /products/{product_id}: Retrieve a specific product by ID.
PUT /products/{product_id}: Update a product by ID.
GET /inventory/status/: Get inventory status for all products.
PUT /inventory/update/{product_id}: Update the inventory count for a product by ID.
GET /inventory-history: Retrieve inventory change history.

# Sales
POST /sales/create: Create a new sale record.
GET /sales/: Retrieve a list of all sales records.
GET /revenue/analysis/: Analyze revenue within a date range.
GET /revenue/comparison/: Compare revenue between two date ranges or categories.
GET /sales/filter/: Filter sales data by date range, product, or category.

# Categories
POST /category/create: Create a new category.
GET /categories/: Retrieve a list of all categories.
PUT /category/{category_id}: Update a category by ID.

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
