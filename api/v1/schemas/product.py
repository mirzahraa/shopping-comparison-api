from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CategoryEnum(str, Enum):
    HOUSEHOLD = "household"
    DAILY_WEAR = "daily_wear"
    OFFICIAL_CLOTHING = "official_clothing"

class PlatformEnum(str, Enum):
    AMAZON = "amazon"
    FLIPKART = "flipkart"
    MYNTRA = "myntra"
    REDTAPE = "redtape"
    VMART = "vmart"

class PriceInfo(BaseModel):
    platform: PlatformEnum
    price: float
    original_price: Optional[float] = None
    discount_percentage: Optional[float] = None
    currency: str = "INR"
    last_updated: datetime
    url: str
    in_stock: bool = True
    delivery_days: Optional[int] = None

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: CategoryEnum
    brand: Optional[str] = None
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    prices: List[PriceInfo]

class Product(ProductBase):
    id: str
    sku: str
    prices: List[PriceInfo]
    average_rating: Optional[float] = None
    total_reviews: Optional[int] = None
    specifications: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    best_price: float
    best_price_platform: PlatformEnum

    class Config:
        from_attributes = True

class ProductSearchResponse(BaseModel):
    total_results: int
    products: List[Product]
    page: int
    page_size: int

class PriceComparison(BaseModel):
    product_id: str
    product_name: str
    category: CategoryEnum
    prices_by_platform: List[PriceInfo]
    price_difference: float
    most_affordable: PlatformEnum
    most_expensive: PlatformEnum
    average_price: float
    last_updated: datetime

class FilterRequest(BaseModel):
    category: Optional[CategoryEnum] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    brand: Optional[str] = None
    min_rating: Optional[float] = None
    platforms: Optional[List[PlatformEnum]] = None
    in_stock: Optional[bool] = True
    page: int = 1
    page_size: int = 20