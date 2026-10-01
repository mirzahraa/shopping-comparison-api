from celery import Celery
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

celery_app = Celery(
    "shopping_comparison_api",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    worker_prefetch_multiplier=1,
)

@celery_app.task(bind=True)
async def scrape_product_prices(self, product_id: str):
    """
    Async task to scrape product prices from all platforms.
    """
    try:
        from scrapers.scraper_factory import ScraperFactory
        
        logger.info(f"Starting price scrape for product {product_id}")
        
        scrapers = ScraperFactory.get_all_scrapers()
        prices = {}
        
        for platform, scraper in scrapers.items():
            try:
                price_data = await scraper.get_product_price(product_id)
                prices[platform] = price_data
            except Exception as e:
                logger.warning(f"Failed to scrape {platform}: {str(e)}")
        
        logger.info(f"Completed price scrape for product {product_id}")
        return prices
    except Exception as e:
        logger.error(f"Error in scrape task: {str(e)}")
        raise

@celery_app.task(bind=True)
async def update_all_prices(self):
    """
    Async task to periodically update all product prices.
    """
    try:
        logger.info("Starting periodic price update")
        # Implementation to fetch all products and update prices
        logger.info("Completed periodic price update")
        return {"status": "completed"}
    except Exception as e:
        logger.error(f"Error in periodic update task: {str(e)}")
        raise

@celery_app.task(bind=True)
async def scrape_reviews(self, product_id: str):
    """
    Async task to scrape product reviews from all platforms.
    """
    try:
        from scrapers.scraper_factory import ScraperFactory
        
        logger.info(f"Starting review scrape for product {product_id}")
        
        scrapers = ScraperFactory.get_all_scrapers()
        reviews = {}
        
        for platform, scraper in scrapers.items():
            try:
                review_data = await scraper.get_product_reviews(product_id)
                reviews[platform] = review_data
            except Exception as e:
                logger.warning(f"Failed to scrape reviews from {platform}: {str(e)}")
        
        logger.info(f"Completed review scrape for product {product_id}")
        return reviews
    except Exception as e:
        logger.error(f"Error in review scrape task: {str(e)}")
        raise