from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from .database import Base


""" SQLALCHEMY MODELS - Object Relational Mapper (ORM)

    * most popular: sqlalchemy
    * different from pydantic model

    - layer of abstraction between dB and API
    - instead of manually defining tables in sql, define tables as python models
    - queries can be made exclusively through python, no sql needed
    - every model defined represents a table
"""


""" table creation

    - column creation(data type)
    - for table migration have to use alembic
    - changes to the code does not update changes to the table
"""


class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="TRUE")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("current_timestamp"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("current_timestamp"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False)  # foreign key

    # relationship (of class) - fetches specific info from other tables
    # returns values from other tables related to this one
    # based on foreign key pointing to this record
    user = relationship("User")


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)  # cannot have duplicated entry
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("current_timestamp"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("current_timestamp"))


class Vote(Base):

    __tablename__ = "votes"

    # both columns are primary key with foreign keys of 2 tables
    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="cascade"), primary_key=True)
