from fastapi import FastAPI, Depends, HTTPException, status,Query
from sqlalchemy import func
from sqlalchemy.orm import Session
import uvicorn

import routes
from models import *
from schemas import *  # You need to import your ProductCreate schema
from db import *

from  routes import *
import config
import constants
from app import app


@app.post(routes.CREATE_CATEGORY, response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(**category.dict())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@app.get(routes.GET_CATEGORIES)
def get_categories( db: Session = Depends(get_db)):

    # If no product_id is provided, retrieve the inventory for all products
    categories = db.query(Category).all()
    categories_data = [{"category_id": category.id, "category_name": category.name} for category in categories]

    return categories_data

# Update a product by ID
@app.put(routes.UPDATE_CATEGORY, response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db)
):
    # Check if the product with the given ID exists
    existing_category = db.query(Category).filter(Category.id == category_id).first()
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category_update.name is not None and category_update.name != 'string':
        existing_category.name = category_update.name

    # Commit the changes to the database
    db.commit()
    db.refresh(existing_category)

    return existing_category


@app.get(routes.PRODUCTS)
def get_inventory( db: Session = Depends(get_db)):

    # If no product_id is provided, retrieve the inventory for all products
    products = db.query(Product).all()
    inventory_data = [{"product_id": product.id, "product name": product.name,'inventory count': product.inventory_count} for product in products]

    return inventory_data


# Create a new product
@app.post(routes.PRODUCT_CREATE, response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Create a new product instance from the incoming data
    new_product = Product(**product.dict())

    # Add the new product to the database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# Retrieve a product by ID
@app.get(routes.SINGLE_PRODUCT, response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    # Query the database for the product with the given ID
    product = db.query(Product).filter(Product.id == product_id).first()

    # Check if the product exists
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# Update a product by ID
@app.put(routes.UPDATE_PRODUCT, response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    # Check if the product with the given ID exists
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update the product fields with the values from the request payload
    if product_update.name is not None and product_update.name != 'string':
        existing_product.name = product_update.name
    if product_update.description is not None and product_update.description != 'string':
        existing_product.description = product_update.description
    if product_update.price is not 0.0 and  product_update.price != 0:
        existing_product.price = product_update.price
    if product_update.inventory_count is not 0:
        existing_product.inventory_count = product_update.inventory_count
    if product_update.category_id is not 0:
        existing_product.category_id = product_update.category_id

    # Commit the changes to the database
    db.commit()
    db.refresh(existing_product)

    return existing_product


@app.get(routes.INVENTORY_STATUS)
def get_inventory_status(
        low_stock_threshold: int = 10,  # You can customize the threshold as needed
        db: Session = Depends(get_db)
):
    # Retrieve all products with inventory counts
    products = db.query(Product).all()

    # Check if any products have inventory below the low stock threshold
    low_stock_products = [product for product in products if product.inventory_count < low_stock_threshold]

    # You can format and return the inventory status as needed
    inventory_status = [
        {
            "product_id": product.id,
            "product_name": product.name,
            "inventory_count": product.inventory_count,
            "low_stock_alert": product.inventory_count < low_stock_threshold
        }
        for product in products
    ]

    return inventory_status

@app.put(routes.UPDATE_PRODUCT_INVENTORY,  response_model=ProductResponse)
def update_inventory(
    product_id: int,
    quantity_change: int,
    db: Session = Depends(get_db)
):
    # Retrieve the product by ID
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    # Update the inventory count based on the quantity_change value
    product.inventory_count += quantity_change



    # Create a record in the inventory history for tracking changes
    inventory_history = InventoryHistory(
        product_id=product.id,
        change_date=datetime.now(),
        quantity_change=quantity_change
    )
    db.add(inventory_history)

    db.commit()

    return product


@app.get(routes.INVENTORY_TRACK_HISTORY)
def inventory_track_history(db: Session = Depends(get_db)):

    history= db.query(InventoryHistory).all()
    inventory_data = [{"product_id": history_item.product_id, "Inventory_change": history_item.quantity_change, 'Date_of_chnage': history_item.change_date.strftime("%Y-%m-%d %H:%M:%S.%f")} for history_item
        in history]

    return inventory_data


#----------------------------------- sale-------------------------------------------

@app.post(routes.CREATE_SALE, response_model=SaleResponse)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    # Check if the product exists
    product = db.query(Product).filter(Product.id == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if there is enough inventory
    if product.inventory_count < sale.quantity_sold:
        raise HTTPException(status_code=400, detail="Insufficient inventory")

    # Deduct the sold quantity from the inventory
    product.inventory_count -= sale.quantity_sold
    db.commit()

    # Create a new sale record
    new_sale = Sale(**sale.dict())
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale

# Retrieve, filter, and analyze sales data
@app.get(routes.GET_SALES)
def get_sales(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    product_id: int = None,
    category_id: int = None,
    db: Session = Depends(get_db)
):
    try:
        # Convert date strings to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    print(start_date,'gfgfgfg', end_date)

    # Build a query to retrieve sales data based on filters
    query = db.query(Sale).filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)

    if product_id is not None:
        query = query.filter(Sale.product_id == product_id)

    if category_id is not None:
        query = query.join(Product, Sale.product_id == Product.id).filter(Product.category_id == category_id)

    sales_data = query.all()

    if not sales_data:
        raise HTTPException(status_code=404, detail="No sales data found for the given filters.")

    # You can format and return the sales data as needed
    formatted_sales_data = [
        {
            "sale_id": sale.id,
            "product_id": sale.product_id,
            "sale_date": sale.sale_date,
            "quantity_sold": sale.quantity_sold,
        }
        for sale in sales_data
    ]

    return formatted_sales_data

# Analyze revenue on a daily, weekly, monthly, and annual basis
@app.get(routes.ANALYZE_REVENUE)
def analyze_revenue(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    interval: str = Query("daily", description="Analysis interval: daily, weekly, monthly, or annual"),
    db: Session = Depends(get_db)
):
    try:
        # Convert date strings to datetime objects
        start_date = tiem_conversion(start_date)
        end_date = tiem_conversion(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    # Determine the date field to group by based on the chosen interval
    date_field = None
    if interval == "daily":
        date_field = Sale.sale_date
    elif interval == "weekly":
        date_field = func.date_trunc('week', Sale.sale_date)
    elif interval == "monthly":
        date_field = func.date_trunc('month', Sale.sale_date)
    elif interval == "annual":
        date_field = func.date_trunc('year', Sale.sale_date)

    # Build a query to calculate revenue for the chosen interval
    revenue_query = db.query(date_field.label("interval"), func.sum(Sale.quantity_sold * Product.price).label("revenue")).\
        join(Product, Sale.product_id == Product.id).\
        filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date).\
        group_by("interval").\
        order_by("interval")

    revenue_data = revenue_query.all()

    if not revenue_data:
        raise HTTPException(status_code=404, detail="No revenue data found for the given filters.")

    # You can format and return the revenue data as needed
    formatted_revenue_data = [
        {
            "interval": entry.interval,
            "revenue": entry.revenue,
        }
        for entry in revenue_data
    ]

    return formatted_revenue_data

def tiem_conversion(date_string):
    datetime_object = datetime.strptime(date_string, "%Y-%m-%d")

    # Add the time components with microseconds set to 0
    datetime_object = datetime_object.replace(hour=0, minute=0, second=0, microsecond=0)

    # Format the datetime object with the desired format
    formatted_datetime = datetime_object.strftime("%Y-%m-%d %H:%M:%S.%f")
    print(formatted_datetime)
    return formatted_datetime


# Ability to compare revenue across different periods and categories
@app.get(routes.REVENUE_COMPARISON)
def compare_revenue(
    start_date1: str = Query(..., description="Start date for period 1 in YYYY-MM-DD format"),
    end_date1: str = Query(..., description="End date for period 1 in YYYY-MM-DD format"),
    start_date2: str = Query(..., description="Start date for period 2 in YYYY-MM-DD format"),
    end_date2: str = Query(..., description="End date for period 2 in YYYY-MM-DD format"),
    category_id: int = None,
    db: Session = Depends(get_db)
):
    try:
        # Convert date strings to datetime objects
        start_date1 = tiem_conversion(start_date1)
        end_date1 = tiem_conversion(end_date1)
        start_date2 = tiem_conversion(start_date2)
        end_date2 = tiem_conversion(end_date2)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    # Build queries to calculate revenue for both periods
    revenue_query1 = db.query(func.sum(Sale.quantity_sold * Product.price).label("revenue")).\
        join(Product, Sale.product_id == Product.id).\
        filter(Sale.sale_date >= start_date1, Sale.sale_date <= end_date1)

    revenue_query2 = db.query(func.sum(Sale.quantity_sold * Product.price).label("revenue")).\
        join(Product, Sale.product_id == Product.id).\
        filter(Sale.sale_date >= start_date2, Sale.sale_date <= end_date2)

    if category_id is not None:
        revenue_query1 = revenue_query1.filter(Product.category_id == category_id)
        revenue_query2 = revenue_query2.filter(Product.category_id == category_id)

    revenue_data1 = revenue_query1.first()
    revenue_data2 = revenue_query2.first()
    print('1111111', revenue_data1)
    if not revenue_data1 or not revenue_data2 :
        raise HTTPException(status_code=404, detail="No revenue data found for the given filters.")

    # Calculate the revenue difference between the two periods
    revenue_difference = revenue_data1.revenue - revenue_data2.revenue

    return {
        "revenue_period_1": revenue_data1.revenue,
        "revenue_period_2": revenue_data2.revenue,
        "revenue_difference": revenue_difference,
    }

# Provide sales data by date range, product, and category
@app.get(routes.SALES_FILTER)
def filter_sales(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    product_id: int = None,
    category_id: int = None,
    db: Session = Depends(get_db)
):
    try:
        # Convert date strings to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    # Build a query to retrieve sales data based on filters
    query = db.query(Sale).filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)

    if product_id is not None:
        query = query.filter(Sale.product_id == product_id)

    if category_id is not None:
        query = query.join(Product, Sale.product_id == Product.id).filter(Product.category_id == category_id)

    sales_data = query.all()

    if not sales_data:
        raise HTTPException(status_code=404, detail="No sales data found for the given filters.")

    # You can format and return the sales data as needed
    formatted_sales_data = [
        {
            "sale_id": sale.id,
            "product_id": sale.product_id,
            "sale_date": sale.sale_date,
            "quantity_sold": sale.quantity_sold,
        }
        for sale in sales_data
    ]

    return formatted_sales_data

if __name__ == "__main__":
    uvicorn.run("main:app", host=config.APP_HOST, port=config.APP_PORT, reload=True)
