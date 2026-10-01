# Migration Guide

This guide covers migrating the project from a mock API implementation to a production-ready system with real data sources.

## Current Status

The project currently includes:
- FastAPI application structure
- Product schemas and endpoints
- Comparison logic
- Platform metadata
- Mock scrapers and services
- Redis caching setup
- Docker Compose environment

## Roadmap to Production

### 1. Replace Mock Data with Real Scrapers

Implement real scrapers for:
- Amazon India
- Flipkart
- Myntra
- Redtape
- V-Mart

Each scraper should:
- Parse product search results
- Extract prices, discounts, availability, reviews
- Handle anti-bot mechanisms
- Respect rate limits
- Cache results appropriately

### 2. Add Database Persistence

Set up real database models and migrations using Alembic:

```bash
pip install alembic
alembic init alembic
```

Then define migration scripts for:
- products
- prices
- price_history
- reviews
- platform_status

### 3. Implement Real Product Search

Replace mock search logic in `services/product_service.py` with:
- Query database indexes
- Merge search results from multiple platforms
- Rank results by price, rating, and relevance
- Normalize data across platforms

### 4. Add Authentication and Authorization

Production requirements:
- JWT-based authentication
- Role-based access control
- Rate limiting per user
- API key management

### 5. Add Observability

Add:
- Structured logging
- Prometheus metrics
- OpenTelemetry tracing
- Error monitoring (Sentry)
- Request correlation IDs

### 6. Add Data Quality Rules

Implement validation for:
- Price normalization (INR, decimal formatting)
- Duplicate detection across platforms
- Product matching between different stores
- Review sentiment analysis

### 7. Add Webhooks and Real-time Updates

Enable event-driven updates for:
- Price drops
- Out-of-stock notifications
- Category refresh jobs
- Platform availability changes

## Recommended Production Stack

- App: FastAPI + Uvicorn
- Database: PostgreSQL
- Cache: Redis
- Search: Elasticsearch/OpenSearch
- Queue: Celery + Redis
- Scraping: Playwright or Selenium + proxy rotation
- Monitoring: Prometheus + Grafana + Sentry

## Example Production Architecture

```text
Client --> API Gateway --> FastAPI App --> PostgreSQL
                      |--> Redis Cache
                      |--> Celery Workers --> Scrapers --> External Stores
                      |--> Search Index
```

## Important Considerations

### Legal/Compliance

Before scraping any website, verify:
- robots.txt compliance
- Terms of service compliance
- Applicable data retention policies
- API terms for affiliate programs

### Performance

Use:
- Async I/O for API requests
- Bulk retrieval for product updates
- Intelligent caching TTLs
- Background jobs for scraper tasks

### Data Normalization

Each platform may return different fields. Standardize to:
- `platform`
- `name`
- `brand`
- `category`
- `price`
- `currency`
- `in_stock`
- `rating`
- `reviews`
- `url`

## Next Milestones

1. Implement real scraping clients
2. Add Alembic migrations
3. Add search indexing
4. Add JWT auth
5. Add production deployment configuration
6. Add CI/CD pipeline
7. Add end-to-end tests

## Suggested Future Features

- Personalized recommendations
- Price alert subscriptions
- Barcode search
- Image similarity matching
- User reviews and ratings
- Affiliate revenue tracking
- Wishlist and cart comparison

## Maintenance Notes

- Update scraper selectors when storefront HTML changes
- Rotate user-agent strings and IPs for scraping
- Monitor external APIs for downtime and rate limits
- Schedule periodic full re-indexing jobs

## Contact

For project support or feature requests:
- GitHub Issues: https://github.com/mirzahraa/shopping-comparison-api/issues
