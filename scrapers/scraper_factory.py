from scrapers.amazon_scraper import AmazonScraper
from scrapers.flipkart_scraper import FlipkartScraper
from scrapers.myntra_scraper import MyntraScraper
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class ScraperFactory:
    """
    Factory class for creating platform-specific scrapers.
    """
    
    _scrapers = {
        "amazon": AmazonScraper,
        "flipkart": FlipkartScraper,
        "myntra": MyntraScraper,
        # Redtape and V-Mart scrapers would follow the same pattern
    }
    
    @classmethod
    def get_scraper(cls, platform: str):
        """
        Get a scraper instance for a specific platform.
        """
        scraper_class = cls._scrapers.get(platform.lower())
        if not scraper_class:
            raise ValueError(f"Scraper not available for platform: {platform}")
        return scraper_class()
    
    @classmethod
    def get_all_scrapers(cls) -> Dict[str, object]:
        """
        Get instances of all available scrapers.
        """
        return {
            platform: scraper_class()
            for platform, scraper_class in cls._scrapers.items()
        }