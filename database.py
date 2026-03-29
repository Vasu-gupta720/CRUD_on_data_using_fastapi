from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


db_url = "postgresql://postgres:vasu%40123@localhost:5432/fastapi_db"
engine = create_engine(db_url)
session = sessionmaker(autocommit = False , autoflush = False , bind = engine)