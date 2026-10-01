from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from api.v1.routes import products, comparison, platforms
from config.settings import settings
from database.connection import init_db

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Shopping Comparison API")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down Shopping Comparison API")

app = FastAPI(
    title="Shopping Comparison API",
    description="Compare products and prices across major e-commerce platforms",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    products.router,
    prefix="/api/v1",
    tags=["products"]
)
app.include_router(
    comparison.router,
    prefix="/api/v1",
    tags=["comparison"]
)
app.include_router(
    platforms.router,
    prefix="/api/v1",
    tags=["platforms"]
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Shopping Comparison API is running"}

@app.get("/")
async def root():
    return {
        "name": "Shopping Comparison API",
        "version": "1.0.0",
        "description": "Compare products and prices across Amazon, Flipkart, Myntra, Redtape, and V mart",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)