from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Determine which database URL to use based on DATABASE_TYPE
if settings.DATABASE_TYPE.lower() == "mysql":
    DATABASE_URL = settings.DATABASE_URL_MYSQL
else:
    DATABASE_URL = settings.DATABASE_URL

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session.
    Use this in FastAPI endpoints to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all tables in the database using Alembic migrations.
    This should be called when the application starts.
    """
    import subprocess
    import sys
    
    try:
        # Run alembic upgrade to ensure database is up to date
        result = subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], 
                              capture_output=True, text=True, cwd=".")
        if result.returncode != 0:
            print(f"Warning: Alembic upgrade failed: {result.stderr}")
            print("Falling back to direct table creation...")
            # Fallback to direct table creation
            Base.metadata.create_all(bind=engine)
        else:
            print("✅ Database tables created/updated via Alembic migrations")
    except Exception as e:
        print(f"Warning: Could not run Alembic migrations: {e}")
        print("Falling back to direct table creation...")
        # Fallback to direct table creation
        Base.metadata.create_all(bind=engine)


def drop_tables():
    """
    Drop all tables in the database using Alembic migrations.
    Use with caution - this will delete all data!
    """
    import subprocess
    import sys
    
    try:
        # Run alembic downgrade to base (removes all tables)
        result = subprocess.run([sys.executable, "-m", "alembic", "downgrade", "base"], 
                              capture_output=True, text=True, cwd=".")
        if result.returncode != 0:
            print(f"Warning: Alembic downgrade failed: {result.stderr}")
            print("Falling back to direct table dropping...")
            # Fallback to direct table dropping
            Base.metadata.drop_all(bind=engine)
        else:
            print("✅ Database tables dropped via Alembic migrations")
    except Exception as e:
        print(f"Warning: Could not run Alembic downgrade: {e}")
        print("Falling back to direct table dropping...")
        # Fallback to direct table dropping
        Base.metadata.drop_all(bind=engine)
