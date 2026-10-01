from fastapi import APIRouter, HTTPException
from api.v1.schemas.product import PlatformEnum
from services.platform_service import PlatformService

router = APIRouter(prefix="/platforms")
platform_service = PlatformService()

@router.get("")
async def get_all_platforms():
    """
    Get list of all supported e-commerce platforms.
    """
    return {
        "platforms": [
            {"name": "amazon", "display_name": "Amazon", "url": "https://www.amazon.in"},
            {"name": "flipkart", "display_name": "Flipkart", "url": "https://www.flipkart.com"},
            {"name": "myntra", "display_name": "Myntra", "url": "https://www.myntra.com"},
            {"name": "redtape", "display_name": "Red Tape", "url": "https://www.redtape.com"},
            {"name": "vmart", "display_name": "V-Mart", "url": "https://www.vmart.com"}
        ],
        "count": 5
    }

@router.get("/{platform}")
async def get_platform_info(platform: PlatformEnum):
    """
    Get detailed information about a specific platform.
    """
    platform_info = await platform_service.get_platform_info(platform)
    
    if not platform_info:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    return platform_info

@router.get("/{platform}/categories")
async def get_platform_categories(platform: PlatformEnum):
    """
    Get available product categories for a specific platform.
    """
    categories = await platform_service.get_categories(platform)
    return {"platform": platform, "categories": categories}

@router.get("/{platform}/status")
async def get_platform_status(platform: PlatformEnum):
    """
    Get current status and statistics for a platform.
    """
    status = await platform_service.get_platform_status(platform)
    return status