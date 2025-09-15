from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Choose database URL based on settings
if settings.DATABASE_TYPE.lower() == "mysql":
    DATABASE_URL = settings.DATABASE_URL_MYSQL
else:
    DATABASE_URL = settings.DATABASE_URL

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


# Create tables
def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)


# Drop tables (for testing)
def drop_tables():
    """Drop all tables in the database"""
    Base.metadata.drop_all(bind=engine)
