import pytest
from unittest.mock import patch, MagicMock
from app.services.article.article import (
    get_all_articles_except_user_articles,
    get_articles_by_user,
    get_article_by_id,
    create_article,
    update_article,
    delete_article
)
from app.models.article.article import Article
from app.models.user.user import User
from app.schemas.article.article import ArticleCreate, ArticleUpdate
from uuid import uuid4

mock_user_id= uuid4()
mock_article_id = uuid4()
mock_article_data = {
    "id": mock_article_id,
    "title": "Test Article",
    "content": "This is a test article.",
    "author_id": mock_user_id
}

class MockArticle:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

@pytest.fixture
def mock_session():
    return MagicMock()

def test_get_all_articles_except_user_articles(mock_session):
    mock_article = MockArticle(**mock_article_data)
    mock_session.query().filter().options().offset().limit().all.return_value = [mock_article]
    mock_session.query().filter().count.return_value = 1
    
    result = get_all_articles_except_user_articles(mock_session, user_id=uuid4())
    
    assert result["articles"][0].title == mock_article_data["title"]
    assert result["total_articles"] == 1

def test_get_articles_by_user(mock_session):
    mock_article = MockArticle(**mock_article_data)
    mock_session.query().filter().options().all.return_value = [mock_article]
    
    result = get_articles_by_user(mock_session, user_id=mock_user_id)
    
    assert len(result) == 1
    assert result[0].title == mock_article_data["title"]

def test_get_article_by_id(mock_session):
    mock_article = MockArticle(**mock_article_data)
    mock_session.query().filter().options().first.return_value = mock_article
    
    result = get_article_by_id(mock_session, id=mock_article_data["id"])
    
    assert result.title == mock_article_data["title"]

def test_create_article(mock_session):
    mock_user = User(id=mock_user_id, email="test@example.com")
    article_create_data = ArticleCreate(
        title="New Article",
        content="This is a new article.",
        labels=[]
    )
    mock_article = MockArticle(**mock_article_data)
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = mock_article
    
    result = create_article(mock_session, article_create_data, current_user=mock_user)
    
    assert result.title == "New Article"

def test_update_article(mock_session):
    mock_user = User(id=mock_user_id, email="test@example.com")
    mock_article = MockArticle(**mock_article_data)
    mock_session.query().filter().first.return_value = mock_article
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = mock_article
    
    article_update_data = ArticleUpdate(
        title="Updated Article",
        content="new content"
    )
    
    result = update_article(mock_session, article_id=mock_article_data["id"], article=article_update_data, current_user=mock_user)
    
    assert result.title == "Updated Article"

def test_delete_article(mock_session):
    mock_article = MockArticle(**mock_article_data)
    mock_session.query().filter().first.return_value = mock_article
    mock_session.commit.return_value = None
    
    result = delete_article(mock_session, article_id=mock_article_data["id"], current_user=User(id=mock_article_data["author_id"]))
    
    assert result.title == "Test Article"
