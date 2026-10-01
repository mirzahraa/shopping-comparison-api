from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """
    Base class for all platform-specific scrapers.
    """
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.timeout = 30
        self.retry_count = 3
    
    @abstractmethod
    async def search_products(self, query: str, category: Optional[str] = None) -> List[dict]:
        """
        Search for products on the platform.
        """
        pass
    
    @abstractmethod
    async def get_product_details(self, product_id: str) -> dict:
        """
        Get detailed product information.
        """
        pass
    
    @abstractmethod
    async def get_product_price(self, product_id: str) -> dict:
        """
        Get current price information for a product.
        """
        pass
    
    @abstractmethod
    async def get_product_reviews(self, product_id: str) -> List[dict]:
        """
        Get customer reviews for a product.
        """
        pass
    
    async def scrape_with_retry(self, func, *args, **kwargs):
        """
        Execute scraping function with retry logic.
        """
        for attempt in range(self.retry_count):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {self.platform_name}: {str(e)}")
                if attempt == self.retry_count - 1:
                    raise