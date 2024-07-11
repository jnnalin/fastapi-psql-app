from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
Base = declarative_base()

import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Date, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    signup_date = Column(Date, nullable=False)

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID, nullable=False)
    order_date = Column(Date, nullable=False)
    total_amount = Column(DECIMAL, nullable=False)

class OrderItem(Base):
    __tablename__ = "order_items"
    order_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID, nullable=False)
    product_id = Column(UUID, nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(DECIMAL, nullable=False)

class Product(Base):
    __tablename__ = "products"
    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class CProduct(Base):
    __tablename__ = 'custom_products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    review_count = Column(Integer, nullable=False)