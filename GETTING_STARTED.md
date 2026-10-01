# Getting Started

## Installation

### Option 1: Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/mirzahraa/shopping-comparison-api.git
cd shopping-comparison-api

# Copy environment file
cp .env.example .env

# Update .env with your API keys
nano .env

# Start services with Docker Compose
docker-compose up -d

# Access the API
Open http://localhost:8000 in your browser
API Documentation: http://localhost:8000/docs
```

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/mirzahraa/shopping-comparison-api.git
cd shopping-comparison-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
# Make sure PostgreSQL is running
psql -U postgres -c "CREATE DATABASE shopping_comparison_db;"

# Setup Redis
# Make sure Redis is running on localhost:6379

# Copy and configure environment
cp .env.example .env
nano .env

# Run the API
uvicorn main:app --reload

# In another terminal, run Celery worker (for async tasks)
celery -A tasks.celery_tasks worker --loglevel=info
```

## Verification

### Health Check
```bash
curl http://localhost:8000/health
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Basic Usage Examples

### 1. Search for Products
```bash
curl "http://localhost:8000/api/v1/products/search?query=t-shirt&category=daily_wear"
```

### 2. Filter Products by Price
```bash
curl "http://localhost:8000/api/v1/products/filter?min_price=500&max_price=1000&platforms=amazon,flipkart"
```

### 3. Get Product Details
```bash
curl "http://localhost:8000/api/v1/products/prod_123"
```

### 4. Compare Products
```bash
curl -X POST "http://localhost:8000/api/v1/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "product_ids": ["prod_123", "prod_456"],
    "platforms": ["amazon", "flipkart"]
  }'
```

### 5. Get Best Deals
```bash
curl "http://localhost:8000/api/v1/compare/best-deals?category=daily_wear&limit=10"
```

### 6. Get Platform Info
```bash
curl "http://localhost:8000/api/v1/platforms/amazon"
```

### 7. Get Price Trends
```bash
curl "http://localhost:8000/api/v1/compare/price-trend/prod_123?days=30"
```

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Running with Hot Reload
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Building Docker Image
```bash
docker build -t shopping-comparison-api:latest .
```

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -U shopping_user -d shopping_comparison_db -c "SELECT 1;"
```

### Redis Connection Issues
```bash
# Check Redis is running
redis-cli ping

# Should return: PONG
```

### Celery Worker Issues
```bash
# Start Celery with verbose logging
celery -A tasks.celery_tasks worker --loglevel=debug
```

## Production Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### Using Docker in Production
```bash
# Build production image
docker build -t shopping-comparison-api:prod .

# Run container
docker run -d \
  --name shopping-api \
  -p 8000:8000 \
  --env-file .env.production \
  shopping-comparison-api:prod
```

### Environment Variables for Production
- Set `DEBUG=False`
- Use strong `SECRET_KEY`
- Configure proper database URLs
- Enable HTTPS
- Set up proper CORS origins
- Use production Redis instance

## API Keys Setup

To enable actual scraping from platforms, you'll need to:

1. **Amazon**: Register for Product Advertising API
2. **Flipkart**: Get API credentials from Flipkart Affiliate Program
3. **Myntra**: Request API access from Myntra Developer Portal
4. **Redtape**: Contact their developer support
5. **V-Mart**: Request API credentials

Add these to your `.env` file:
```
AMAZON_API_KEY=your_key
FLIPKART_API_KEY=your_key
MYNTRA_API_KEY=your_key
REDTAPE_API_KEY=your_key
VMART_API_KEY=your_key
```

## Next Steps

1. Review the [API Documentation](docs/API.md)
2. Implement actual platform scrapers (currently using mocks)
3. Set up database migrations
4. Configure authentication (JWT/OAuth2)
5. Add comprehensive tests
6. Deploy to production

## Support

For issues and questions:
- GitHub Issues: https://github.com/mirzahraa/shopping-comparison-api/issues
- Documentation: See `/docs` folder
