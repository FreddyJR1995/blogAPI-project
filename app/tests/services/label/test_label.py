import pytest
from unittest.mock import MagicMock
from app.services.label.label import get_all_labels
from app.models.label.label import Label
from uuid import uuid4
from sqlalchemy.orm import Session

mock_label_id = uuid4()
mock_label_data = {
    "id": mock_label_id,
    "text": "Test Label"
}

class MockLabel:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)

def test_get_all_labels(mock_session):
    mock_label = MockLabel(**mock_label_data)
    mock_session.query.return_value = [mock_label]
    
    result = get_all_labels(mock_session)
    assert len(result) == 1
    assert result[0].id == mock_label_data["id"]
    assert result[0].text == "Test Label"
