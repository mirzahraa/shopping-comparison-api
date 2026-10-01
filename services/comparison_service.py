from typing import List, Optional
from datetime import datetime, timedelta
from api.v1.schemas.product import PriceComparison, PlatformEnum
import logging

logger = logging.getLogger(__name__)

class ComparisonService:
    """Service for price comparison and analysis"""
    
    async def compare_products(
        self,
        product_ids: List[str],
        platforms: Optional[List[PlatformEnum]] = None
    ) -> List[PriceComparison]:
        """
        Compare prices of multiple products across platforms.
        """
        try:
            comparisons = []
            for product_id in product_ids:
                comparison = await self._build_comparison(product_id, platforms)
                if comparison:
                    comparisons.append(comparison)
            return comparisons
        except Exception as e:
            logger.error(f"Error comparing products: {str(e)}")
            raise
    
    async def get_price_trend(self, product_id: str, days: int = 30) -> List[dict]:
        """
        Get historical price trend data.
        """
        try:
            trend_data = await self._fetch_price_history(product_id, days)
            return trend_data
        except Exception as e:
            logger.error(f"Error fetching price trend: {str(e)}")
            raise
    
    async def get_best_deals(
        self,
        category: Optional[str] = None,
        limit: int = 20,
        min_discount: float = 0
    ) -> List[dict]:
        """
        Get best deals/discounts available.
        """
        try:
            deals = await self._fetch_best_deals(category, limit, min_discount)
            return deals
        except Exception as e:
            logger.error(f"Error fetching deals: {str(e)}")
            raise
    
    async def analyze_platforms(self, category: Optional[str] = None) -> dict:
        """
        Analyze platform pricing patterns and strategies.
        """
        try:
            analysis = await self._perform_platform_analysis(category)
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing platforms: {str(e)}")
            raise
    
    async def _build_comparison(self, product_id: str, platforms) -> Optional[PriceComparison]:
        """Build comparison data for a product"""
        from services.product_service import ProductService
        product_service = ProductService()
        
        product = await product_service.get_product_by_id(product_id)
        if not product:
            return None
        
        prices = product.prices
        if platforms:
            prices = [p for p in prices if p.platform in platforms]
        
        if not prices:
            return None
        
        sorted_prices = sorted(prices, key=lambda x: x.price)
        avg_price = sum(p.price for p in prices) / len(prices)
        
        return PriceComparison(
            product_id=product_id,
            product_name=product.name,
            category=product.category,
            prices_by_platform=prices,
            price_difference=sorted_prices[-1].price - sorted_prices[0].price,
            most_affordable=sorted_prices[0].platform,
            most_expensive=sorted_prices[-1].platform,
            average_price=avg_price,
            last_updated=datetime.now()
        )
    
    async def _fetch_price_history(self, product_id: str, days: int) -> List[dict]:
        """Mock price history - replace with actual database query"""
        trend_data = []
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i)
            trend_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "amazon_price": 599.00 + (i * 5),
                "flipkart_price": 549.00 + (i * 3),
                "myntra_price": 629.00 + (i * 2),
                "average_price": 592.33 + (i * 3.33)
            })
        return trend_data
    
    async def _fetch_best_deals(self, category: Optional[str], limit: int, min_discount: float) -> List[dict]:
        """Mock best deals - replace with actual database query"""
        deals = [
            {
                "product_id": f"prod_{i}",
                "name": f"Premium Product {i}",
                "platform": "flipkart" if i % 2 == 0 else "amazon",
                "current_price": 500 + (i * 50),
                "original_price": 1000 + (i * 50),
                "discount_percentage": 50 - (i * 2),
                "savings": 500 + (i * 50),
                "rating": 4.0 + (i * 0.1),
                "reviews": 100 + (i * 50)
            }
            for i in range(1, limit + 1)
        ]
        return sorted(deals, key=lambda x: x['discount_percentage'], reverse=True)[:limit]
    
    async def _perform_platform_analysis(self, category: Optional[str]) -> dict:
        """Mock platform analysis - replace with actual analysis"""
        platforms_stats = {
            "amazon": {
                "avg_price": 599.50,
                "avg_discount": 25,
                "products_count": 15000,
                "avg_rating": 4.3,
                "delivery_days": 2,
                "price_competitiveness": "High"
            },
            "flipkart": {
                "avg_price": 559.75,
                "avg_discount": 32,
                "products_count": 12000,
                "avg_rating": 4.2,
                "delivery_days": 3,
                "price_competitiveness": "Very High"
            },
            "myntra": {
                "avg_price": 629.00,
                "avg_discount": 20,
                "products_count": 8000,
                "avg_rating": 4.4,
                "delivery_days": 2,
                "price_competitiveness": "Medium"
            },
            "redtape": {
                "avg_price": 799.00,
                "avg_discount": 15,
                "products_count": 3000,
                "avg_rating": 4.5,
                "delivery_days": 3,
                "price_competitiveness": "Low"
            },
            "vmart": {
                "avg_price": 549.25,
                "avg_discount": 28,
                "products_count": 5000,
                "avg_rating": 4.1,
                "delivery_days": 4,
                "price_competitiveness": "High"
            }
        }
        
        return {
            "category": category or "all",
            "analysis_date": datetime.now().isoformat(),
            "platforms": platforms_stats,
            "summary": {
                "cheapest_platform": "vmart",
                "most_expensive_platform": "redtape",
                "best_for_discounts": "flipkart",
                "best_for_ratings": "redtape",
                "fastest_delivery": "amazon"
            }
        }