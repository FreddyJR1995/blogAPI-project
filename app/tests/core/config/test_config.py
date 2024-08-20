import os
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def test_config():
    assert SECRET_KEY == os.getenv("SECRET_KEY")
    assert ALGORITHM == "HS256"
    assert ACCESS_TOKEN_EXPIRE_MINUTES == 30
