from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.utils.settings import settings


# Database connection
engine = create_engine(
    settings.DB_CONNECTION
)


# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for SQLAlchemy models
Base = declarative_base()


# Dependency for FastAPI
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()