from fastapi import APIRouter, HTTPException, Body
from typing import List
from api.v1.schemas.product import PriceComparison, PlatformEnum
from services.comparison_service import ComparisonService
from services.cache_service import CacheService

router = APIRouter(prefix="/compare")
comparison_service = ComparisonService()
cache_service = CacheService()

@router.post("", response_model=List[PriceComparison])
async def compare_products(
    product_ids: List[str] = Body(..., embed=True, description="List of product IDs to compare"),
    platforms: List[PlatformEnum] = Body(None, embed=True, description="Specific platforms to compare")
):
    """
    Compare prices of multiple products across platforms.
    
    Request body:
    ```json
    {
        "product_ids": ["prod_123", "prod_456"],
        "platforms": ["amazon", "flipkart", "myntra"]
    }
    ```
    """
    if not product_ids:
        raise HTTPException(status_code=400, detail="product_ids cannot be empty")
    
    cache_key = f"comparison:{':'.join(sorted(product_ids))}:{':'.join(sorted([p.value for p in platforms] if platforms else []))}"
    cached_result = await cache_service.get(cache_key)
    
    if cached_result:
        return cached_result
    
    comparison_results = await comparison_service.compare_products(
        product_ids=product_ids,
        platforms=platforms
    )
    
    await cache_service.set(cache_key, comparison_results)
    return comparison_results

@router.get("/price-trend/{product_id}")
async def get_price_trend(product_id: str, days: int = 30):
    """
    Get historical price trends for a product.
    
    - **product_id**: Product ID
    - **days**: Number of days to look back (default: 30)
    """
    trend = await comparison_service.get_price_trend(product_id, days)
    
    if not trend:
        raise HTTPException(status_code=404, detail="Price trend data not found")
    
    return {
        "product_id": product_id,
        "period_days": days,
        "trend_data": trend
    }

@router.get("/best-deals")
async def get_best_deals(
    category: str = None,
    limit: int = 20,
    min_discount: float = 0
):
    """
    Get products with the best discounts.
    
    - **category**: Product category
    - **limit**: Number of results
    - **min_discount**: Minimum discount percentage
    """
    deals = await comparison_service.get_best_deals(
        category=category,
        limit=limit,
        min_discount=min_discount
    )
    
    return {"deals": deals, "count": len(deals)}

@router.get("/platform-analysis")
async def get_platform_analysis(category: str = None):
    """
    Analyze platform pricing strategies and availability.
    """
    analysis = await comparison_service.analyze_platforms(category)
    return analysis