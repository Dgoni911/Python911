import pytest
import requests
import json
from typing import Dict, Any

@pytest.fixture
def base_url() -> str:
    return "https://jsonplaceholder.typicode.com"

@pytest.fixture
def headers() -> Dict[str, str]:
    return {
        "Content-Type": "application/json; charset=UTF-8"
    }

@pytest.fixture
def sample_post_data() -> Dict[str, Any]:
    return {
        "title": "Test Post Title",
        "body": "This is a test post body content for API testing",
        "userId": 1
    }

@pytest.fixture
def existing_post_id() -> int:
    return 1

@pytest.fixture
def non_existent_post_id() -> int:
    return 999