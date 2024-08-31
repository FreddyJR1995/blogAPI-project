from sqlalchemy.orm import Session, joinedload
from app.models.article.article import Article
from app.models.label.label import Label
from app.schemas.article.article import ArticleCreate, ArticleUpdate
from app.models.user.user import User
from fastapi import HTTPException, status

def get_all_articles_except_user_articles(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    articles = db.query(Article).filter(Article.author_id != user_id).options(joinedload(Article.author)).offset(skip).limit(limit).all()
    return articles

def get_articles_by_user(db: Session, user_id: int):
    return db.query(Article).filter(Article.author_id == user_id).options(joinedload(Article.author)).all()

def get_article_by_id(db: Session, id: int):
    return db.query(Article).filter(Article.id == id).options(joinedload(Article.author)).first()

def create_article(db: Session, article: ArticleCreate, current_user: User):
    db_article = Article(title=article.title, content=article.content, author_id=current_user.id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    for label in article.labels:
        db_label = db.query(Label).filter(Label.text == label.text).first()
        if not db_label:
            db_label = Label(text=label.text)
            db.add(db_label)
            db.commit()
            db.refresh(db_label)
        db_article.labels.append(db_label)
    db.commit()
    return db_article

def update_article(db: Session, article_id: int, article: ArticleUpdate, current_user: User):
    db_article = db.query(Article).filter(Article.id == article_id, Article.author_id == current_user.id).first()
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    for key, value in article.dict(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article

def delete_article(db: Session, article_id: int, current_user: User):
    db_article = db.query(Article).filter(Article.id == article_id, Article.author_id == current_user.id).first()
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    db.delete(db_article)
    db.commit()
    return db_article
