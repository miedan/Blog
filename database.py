from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

sqlalchemy_database_url = "postgresql://postgres:123@localhost:5000/products"
# DATABASE_URL = "postgresql://postgres:123@localhost:5432/products"

engine = create_engine(sqlalchemy_database_url)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()