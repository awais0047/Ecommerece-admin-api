from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Product, Sale, Category
from datetime import datetime

# Sample data for product categories
categories_data = [
    {"name": "Electronics"},
    {"name": "Clothing"},
    {"name": "Books"},
    # Add more categories as needed
]

# Sample data for products
products_data = [
    {"name": "Smartphone", "description": "High-end smartphone", "price": 699.99, "inventory_count": 100, "category_id": 1},
    {"name": "Laptop", "description": "Powerful laptop", "price": 1299.99, "inventory_count": 50, "category_id": 1},
    {"name": "T-shirt", "description": "Cotton t-shirt", "price": 19.99, "inventory_count": 200, "category_id": 2},
    # Add more products as needed
]

# Sample data for sales
sales_data = [
    {"product_id": 1, "sale_date": datetime.now(), "quantity_sold": 5},
    {"product_id": 2, "sale_date": datetime.now(), "quantity_sold": 2},
    {"product_id": 3, "sale_date": datetime.now(), "quantity_sold": 10},
    # Add more sales data as needed
]

# Function to populate categories
def populate_categories(db):
    for category in categories_data:
        db.add(Category(**category))

# Function to populate products
def populate_products(db):
    for product in products_data:
        db.add(Product(**product))

# Function to populate sales
def populate_sales(db):
    for sale in sales_data:
        db.add(Sale(**sale))

# Main function to populate the database with demo data
def populate_demo_data():
    db = SessionLocal()

    try:
        # Populate categories
        populate_categories(db)

        # Populate products
        populate_products(db)

        # Populate sales
        populate_sales(db)

        db.commit()
        print("Demo data has been successfully inserted into the database.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_demo_data()
