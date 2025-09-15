from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import create_tables
from app.api import auth, users, search, explore, dashboard, seed, keywords
from app.utils.seeder import seed_initial_data


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting up TikTok Database API...")
    create_tables()
    
    # Seed initial data if needed
    try:
        seed_initial_data()
        logger.info("Initial data seeded successfully")
    except Exception as e:
        logger.warning(f"Failed to seed initial data: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down TikTok Database API...")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A production-grade FastAPI backend for TikTok database management",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(search.router, prefix=settings.API_V1_STR)
app.include_router(explore.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)
app.include_router(seed.router, prefix=settings.API_V1_STR)
app.include_router(keywords.router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to TikTok Database API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
