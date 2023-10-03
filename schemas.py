# schemas.py
from pydantic import BaseModel
from models import *
from typing import Optional

# Schema for creating a new product
from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    inventory_count: int
    category_id: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    inventory_count: int
    category_id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    inventory_count: Optional[int] = None
    category_id: Optional[int] = None


# Schema for creating a new sale record
class SaleCreate(BaseModel):
    product_id: int
    sale_date: datetime
    quantity_sold: int


class SaleResponse(BaseModel):
    id: int
    product_id: int
    sale_date: datetime
    quantity_sold: int


class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
