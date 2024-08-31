from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.article.article import Article, ArticleCreate, ArticleUpdate
from app.models.user.user import User
from app.utils.db import get_db
from app.routers.user.user import get_current_user
from app.services.article.article import (
    get_all_articles_except_user_articles,
    get_articles_by_user,
    create_article,
    update_article,
    delete_article,
    get_article_by_id
)

router = APIRouter()

@router.get("/articles/", response_model=List[Article])
def fetch_all_articles_except_user_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    articles = get_all_articles_except_user_articles(db, current_user.id, skip, limit)
    return articles

@router.get("/articles/user/", response_model=List[Article])
def fetch_articles_by_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_articles_by_user(db, current_user.id)

@router.get("/articles/{article_id}", response_model=Article)
def fetch_article_by_id(article_id: int, db: Session= Depends(get_db)):
    return get_article_by_id(db, article_id)

@router.post("/articles/", response_model=Article)
def create_new_article(article: ArticleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_article(db, article, current_user)

@router.put("/articles/{article_id}", response_model=Article)
def modify_article(article_id: int, article: ArticleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_article(db, article_id, article, current_user)

@router.delete("/articles/{article_id}", response_model=Article)
def remove_article(article_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_article(db, article_id, current_user)
