from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.engine import reflection
import endpoint
from app import app
from models import Base


# Configure your PostgreSQL database URL
POSTGRESQL_DATABASE_URL = endpoint.POSTGRESQL_DATABASE_URL

# Create a SQLAlchemy engine
engine = create_engine(POSTGRESQL_DATABASE_URL)

# Create a Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models

# Create the database tables
Base.metadata.create_all(bind=engine)

# Set up the database query object
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Set up SQLAlchemy's automap functionality (if needed)
base = automap_base()
base.prepare(engine, reflect=True)
insp = reflection.Inspector.from_engine(engine)
dbTables = insp.get_table_names()

db = get_db()