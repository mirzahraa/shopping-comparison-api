# API Documentation

## Authentication

Currently, the API is open (no authentication required). In production, implement JWT or OAuth2.

## Base URL

```
http://localhost:8000/api/v1
```

## Response Format

All responses are in JSON format.

## Error Handling

Errors follow standard HTTP status codes:
- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Endpoints

### Products

#### Search Products
```
GET /products/search?query=shirt&category=daily_wear&page=1&page_size=20
```

**Parameters:**
- `query` (string, required): Search term
- `category` (string, optional): Category filter (household, daily_wear, official_clothing)
- `page` (integer, optional): Page number (default: 1)
- `page_size` (integer, optional): Items per page (default: 20, max: 100)

**Response:**
```json
{
  "total_results": 1250,
  "products": [
    {
      "id": "prod_123",
      "sku": "SKU00123",
      "name": "Premium Cotton T-Shirt",
      "description": "Comfortable cotton t-shirt",
      "category": "daily_wear",
      "brand": "BrandX",
      "image_url": "https://...",
      "prices": [
        {
          "platform": "amazon",
          "price": 599.00,
          "original_price": 799.00,
          "discount_percentage": 25,
          "currency": "INR",
          "in_stock": true,
          "delivery_days": 2,
          "url": "https://amazon.in/...",
          "last_updated": "2026-10-01T11:50:00Z"
        }
      ],
      "average_rating": 4.5,
      "total_reviews": 2150,
      "best_price": 549.00,
      "best_price_platform": "flipkart"
    }
  ],
  "page": 1,
  "page_size": 20
}
```

#### Filter Products
```
GET /products/filter?category=daily_wear&min_price=500&max_price=5000&min_rating=4.0&platforms=amazon,flipkart&page=1
```

**Parameters:**
- `category` (string, optional): Product category
- `min_price` (float, optional): Minimum price
- `max_price` (float, optional): Maximum price
- `brand` (string, optional): Brand filter
- `min_rating` (float, optional): Minimum rating (0-5)
- `platforms` (string, optional): Comma-separated platform names
- `in_stock` (boolean, optional): Only in-stock items (default: true)
- `page` (integer, optional): Page number
- `page_size` (integer, optional): Items per page

#### Get Product Details
```
GET /products/{product_id}
```

**Response:** Product object with all details and prices

#### Get Product Prices
```
GET /products/{product_id}/prices
```

**Response:**
```json
{
  "product_id": "prod_123",
  "prices": [
    {
      "platform": "amazon",
      "price": 599.00,
      "original_price": 799.00,
      "discount": "25%",
      "delivery_days": 2,
      "in_stock": true,
      "url": "https://amazon.in/..."
    }
  ],
  "best_price": 549.00,
  "average_price": 592.33
}
```

#### Get Product Reviews
```
GET /products/{product_id}/reviews?platform=amazon
```

### Comparison

#### Compare Products
```
POST /compare
```

**Request Body:**
```json
{
  "product_ids": ["prod_123", "prod_456"],
  "platforms": ["amazon", "flipkart", "myntra"]
}
```

**Response:**
```json
[
  {
    "product_id": "prod_123",
    "product_name": "Premium Cotton T-Shirt",
    "category": "daily_wear",
    "prices_by_platform": [...],
    "price_difference": 80.00,
    "most_affordable": "flipkart",
    "most_expensive": "myntra",
    "average_price": 592.33,
    "last_updated": "2026-10-01T11:50:00Z"
  }
]
```

#### Price Trend
```
GET /compare/price-trend/{product_id}?days=30
```

**Response:**
```json
{
  "product_id": "prod_123",
  "period_days": 30,
  "trend_data": [
    {
      "date": "2026-09-01",
      "amazon_price": 599.00,
      "flipkart_price": 549.00,
      "myntra_price": 629.00,
      "average_price": 592.33
    }
  ]
}
```

#### Best Deals
```
GET /compare/best-deals?category=daily_wear&limit=20&min_discount=20
```

**Response:**
```json
{
  "deals": [
    {
      "product_id": "prod_123",
      "name": "Premium Product",
      "platform": "flipkart",
      "current_price": 550.00,
      "original_price": 1000.00,
      "discount_percentage": 45,
      "savings": 450.00,
      "rating": 4.5,
      "reviews": 2150
    }
  ],
  "count": 20
}
```

#### Platform Analysis
```
GET /compare/platform-analysis?category=daily_wear
```

**Response:**
```json
{
  "category": "daily_wear",
  "analysis_date": "2026-10-01T11:50:00Z",
  "platforms": {
    "amazon": {
      "avg_price": 599.50,
      "avg_discount": 25,
      "products_count": 15000,
      "avg_rating": 4.3,
      "delivery_days": 2,
      "price_competitiveness": "High"
    }
  },
  "summary": {
    "cheapest_platform": "vmart",
    "most_expensive_platform": "redtape",
    "best_for_discounts": "flipkart",
    "best_for_ratings": "redtape",
    "fastest_delivery": "amazon"
  }
}
```

### Platforms

#### Get All Platforms
```
GET /platforms
```

#### Get Platform Info
```
GET /platforms/{platform}
```

**Response:**
```json
{
  "name": "Amazon India",
  "url": "https://www.amazon.in",
  "established": 2010,
  "categories": ["household", "daily_wear", "official_clothing"],
  "strengths": ["Fast delivery", "Wide selection", "Good customer service"],
  "currency": "INR"
}
```

#### Get Platform Categories
```
GET /platforms/{platform}/categories
```

#### Get Platform Status
```
GET /platforms/{platform}/status
```

**Response:**
```json
{
  "platform": "amazon",
  "name": "Amazon India",
  "status": "operational",
  "total_products": 50000,
  "last_update": "2026-10-01T11:50:00Z",
  "average_response_time_ms": 250,
  "availability_percentage": 99.8,
  "active_deals": 150,
  "customer_satisfaction": 4.3
}
```

## Rate Limiting

API requests are rate-limited to prevent abuse. Current limits:
- 100 requests per minute per IP

## Caching

Responses are cached using Redis for performance:
- Search results: 1 hour
- Product details: 2 hours
- Price data: 30 minutes
- Platform status: 15 minutes

## Webhook Support

For real-time price updates, you can subscribe to webhooks:

```
POST /webhooks/subscribe
{
  "event": "price_drop",
  "product_id": "prod_123",
  "threshold": 100.00,
  "url": "https://your-app.com/webhook"
}
```