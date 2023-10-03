# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    inventory_count = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))

    sales = relationship('Sale', back_populates='product')
    category = relationship("Category", back_populates="products")
    inventory_history = relationship("InventoryHistory", back_populates="product")



class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    products = relationship("Product", back_populates="category")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    sale_date = Column(DateTime, default=datetime.now, nullable=False)
    quantity_sold = Column(Integer)

    product = relationship("Product", back_populates="sales")


class InventoryHistory(Base):
    __tablename__ = "inventory_history"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    change_date = Column(DateTime, default=datetime.now, nullable=False)
    quantity_change = Column(Integer, nullable=False)

    product = relationship("Product", back_populates="inventory_history")
