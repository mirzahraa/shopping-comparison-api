from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, Boolean, Text
from sqlalchemy.sql import func
from database.connection import Base
from datetime import datetime

class ProductModel(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    category = Column(String, index=True)
    brand = Column(String, index=True)
    image_url = Column(String)
    average_rating = Column(Float)
    total_reviews = Column(Integer)
    specifications = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class PriceModel(Base):
    __tablename__ = "prices"
    
    id = Column(String, primary_key=True, index=True)
    product_id = Column(String, index=True)
    platform = Column(String, index=True)
    price = Column(Float, index=True)
    original_price = Column(Float)
    discount_percentage = Column(Float)
    currency = Column(String, default="INR")
    in_stock = Column(Boolean, default=True)
    delivery_days = Column(Integer)
    product_url = Column(String)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now())

class PriceHistoryModel(Base):
    __tablename__ = "price_history"
    
    id = Column(String, primary_key=True, index=True)
    product_id = Column(String, index=True)
    platform = Column(String, index=True)
    price = Column(Float)
    date = Column(DateTime, index=True)
    created_at = Column(DateTime, server_default=func.now())

class ReviewModel(Base):
    __tablename__ = "reviews"
    
    id = Column(String, primary_key=True, index=True)
    product_id = Column(String, index=True)
    platform = Column(String, index=True)
    rating = Column(Float)
    review_text = Column(Text)
    reviewer_name = Column(String)
    verified_purchase = Column(Boolean)
    helpful_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

class PlatformStatusModel(Base):
    __tablename__ = "platform_status"
    
    id = Column(String, primary_key=True, index=True)
    platform = Column(String, unique=True, index=True)
    status = Column(String)  # operational, degraded, down
    total_products = Column(Integer)
    average_response_time_ms = Column(Float)
    availability_percentage = Column(Float)
    active_deals = Column(Integer)
    last_checked = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now())