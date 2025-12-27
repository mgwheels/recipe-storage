from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import DATABASE_URL


# Database setup
Base = declarative_base()
Engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
