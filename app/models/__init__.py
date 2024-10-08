import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

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
    from app.models.user import user
    from app.models.article import article
    from app.models.label import label
    from app.models.article_label import article_label
    from app.models.comment import comment
    Base.metadata.create_all(bind=engine)
