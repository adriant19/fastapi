from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# using environment variables

""" postgresql

install: brew install postgresql
create: CREATE USER postgres
database: CREATE database postgres

commands:
    \? list all the commands
    \l list databases
    \conninfo display information about current connection
    \c [DBNAME] connect to new database, e.g., \c template1
    \dt list tables of the public schema
    \dt <schema-name>.* list tables of certain schema, e.g., \dt public.*
    \dt *.* list tables of all schemas
    Then you can run SQL statements, e.g., SELECT * FROM my_table;(Note: a statement must be terminated with semicolon ;)
    \q quit psql

"""

SQLALCHEMY_DATABASE_URL = "postgresql://{db_username}:{db_password}@{host_name}:{db_port}/{db_name}".format(
    db_username=settings.DATABASE_USERNAME,
    db_password=settings.DATABASE_PASSWORD,
    host_name=settings.DATABASE_HOSTNAME,
    db_port=settings.DATABASE_PORT,
    db_name=settings.DATABASE_NAME
)

# talk to database requires a session

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    # get connnection to db

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
