from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional, List
from api.v1.schemas.product import (
    Product,
    ProductSearchResponse,
    FilterRequest,
    CategoryEnum,
    PlatformEnum
)
from services.product_service import ProductService
from services.cache_service import CacheService

router = APIRouter(prefix="/products")
product_service = ProductService()
cache_service = CacheService()

@router.get("/search", response_model=ProductSearchResponse)
async def search_products(
    query: str = Query(..., min_length=1, description="Product search query"),
    category: Optional[CategoryEnum] = Query(None, description="Product category"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page")
):
    """
    Search for products across all platforms.
    
    - **query**: Search term (required)
    - **category**: Filter by category (household, daily_wear, official_clothing)
    - **page**: Page number for pagination
    - **page_size**: Number of results per page
    """
    cache_key = f"search:{query}:{category}:{page}:{page_size}"
    cached_result = await cache_service.get(cache_key)
    
    if cached_result:
        return cached_result
    
    results = await product_service.search_products(
        query=query,
        category=category,
        page=page,
        page_size=page_size
    )
    
    await cache_service.set(cache_key, results)
    return results

@router.get("/filter", response_model=ProductSearchResponse)
async def filter_products(
    category: Optional[CategoryEnum] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    brand: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    platforms: Optional[str] = Query(None, description="Comma-separated platform names"),
    in_stock: bool = Query(True),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    Filter products by various criteria.
    
    - **category**: Product category
    - **min_price/max_price**: Price range
    - **brand**: Brand filter
    - **min_rating**: Minimum rating (0-5)
    - **platforms**: Comma-separated list of platforms (amazon,flipkart,myntra,redtape,vmart)
    - **in_stock**: Only show in-stock items
    """
    platform_list = None
    if platforms:
        platform_list = [p.strip() for p in platforms.split(",")]
    
    cache_key = f"filter:{category}:{min_price}:{max_price}:{brand}:{min_rating}:{platforms}:{in_stock}:{page}:{page_size}"
    cached_result = await cache_service.get(cache_key)
    
    if cached_result:
        return cached_result
    
    results = await product_service.filter_products(
        category=category,
        min_price=min_price,
        max_price=max_price,
        brand=brand,
        min_rating=min_rating,
        platforms=platform_list,
        in_stock=in_stock,
        page=page,
        page_size=page_size
    )
    
    await cache_service.set(cache_key, results)
    return results

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """
    Get detailed information about a specific product.
    """
    cache_key = f"product:{product_id}"
    cached_product = await cache_service.get(cache_key)
    
    if cached_product:
        return cached_product
    
    product = await product_service.get_product_by_id(product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    await cache_service.set(cache_key, product)
    return product

@router.get("/{product_id}/prices")
async def get_product_prices(product_id: str):
    """
    Get pricing information for a product across all platforms.
    """
    prices = await product_service.get_product_prices(product_id)
    
    if not prices:
        raise HTTPException(status_code=404, detail="Product prices not found")
    
    return {
        "product_id": product_id,
        "prices": prices,
        "best_price": min(p["price"] for p in prices),
        "average_price": sum(p["price"] for p in prices) / len(prices)
    }

@router.get("/{product_id}/reviews")
async def get_product_reviews(product_id: str, platform: Optional[PlatformEnum] = None):
    """
    Get reviews for a product from specific platforms.
    """
    reviews = await product_service.get_product_reviews(product_id, platform)
    return {"product_id": product_id, "reviews": reviews}