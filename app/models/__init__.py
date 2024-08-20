import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_HOST=os.environ.get("DATABASE_HOST")
DB_USER=os.environ.get("DATABASE_USER")
DB_NAME=os.environ.get("DATABASE_NAME")
DB_PASSWORD=os.environ.get("DATABASE_PASSWORD")

DATABASE_URL = "postgresql://{username}:{password}@{host}:{port}/{db_name}".format(
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port="5432",
        db_name=DB_NAME,
    )
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    import app.models.user
    import app.models.article
    import app.models.label
    Base.metadata.create_all(bind=engine)
