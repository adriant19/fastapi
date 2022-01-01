from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# using environment variables
SQLALCHEMY_DATABASE_URL = f"sqlite:///./{settings.DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# talk to database requires a session

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    # get connnection to db

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
