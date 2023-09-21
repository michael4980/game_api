import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
import pytest
from httpx import AsyncClient


@pytest.fixture
async def test_app():
    yield AsyncClient(app=app, base_url="http://test", headers={"Authorization": f"Bearer {os.getenv('CLIENT_TOKEN')}"})
