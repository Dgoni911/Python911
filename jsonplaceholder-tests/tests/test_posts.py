import pytest
import requests
import time
from typing import Dict, Any


class TestPostOperations:
    
    @pytest.fixture
    def new_post_data(self) -> Dict[str, Any]:
        return {
            "title": "Test Post Title",
            "body": "Test post body content",
            "userId": 1
        }
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        start_time = time.time()
        response = requests.request(method, url, **kwargs)
        response_time = time.time() - start_time
        
        print(f"\n{method} {url}")
        print(f"Статус: {response.status_code}, Время: {response_time:.2f}с")
        
        if response.text:
            print(f"Ответ: {response.json()}")
        
        return response
    
    def test_successful_post_creation(self, base_url: str, new_post_data: Dict[str, Any]) -> None:
        response = self._make_request('POST', f"{base_url}/posts", 
                                     json=new_post_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert all(k in data for k in ['id', 'title', 'body', 'userId'])
        assert data['title'] == new_post_data['title']
        assert data['body'] == new_post_data['body']
        assert data['userId'] == new_post_data['userId']
    
    def test_successful_post_update(self, base_url: str) -> None:
        update_data = {
            "id": 1,
            "title": "Updated Title",
            "body": "Updated body content",
            "userId": 2
        }
        
        response = self._make_request('PUT', f"{base_url}/posts/1", 
                                     json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data == update_data
    
    def test_successful_post_deletion(self, base_url: str) -> None:

        get_response = requests.get(f"{base_url}/posts/1")
        assert get_response.status_code == 200
        
        response = self._make_request('DELETE', f"{base_url}/posts/1")
        
        assert response.status_code == 200
        
        if response.text:
            assert response.json() == {}


class TestExtendedPostOperations:
    
    def test_create_and_verify_post(self, base_url: str) -> None:
        post_data = {
            "title": "New Test Post",
            "body": "Content of new post",
            "userId": 1
        }
        
        create_response = requests.post(f"{base_url}/posts", json=post_data)
        assert create_response.status_code == 201
        
        created_post = create_response.json()
        post_id = created_post['id']
        
        get_response = requests.get(f"{base_url}/posts/{post_id}")
        assert get_response.status_code == 200
        
        retrieved_post = get_response.json()
        assert retrieved_post['title'] == post_data['title']
    
    def test_update_and_verify_post(self, base_url: str) -> None:
        update_data = {
            "id": 1,
            "title": "Completely New Title",
            "body": "Completely new content",
            "userId": 999
        }
        
        update_response = requests.put(f"{base_url}/posts/1", json=update_data)
        assert update_response.status_code == 200
        
        updated_post = update_response.json()
        assert updated_post == update_data
    
    def test_delete_and_verify_post(self, base_url: str) -> None:
    
        delete_response = requests.delete(f"{base_url}/posts/1")
        assert delete_response.status_code == 200
        
        get_response = requests.get(f"{base_url}/posts/1")
        assert get_response.status_code == 200


def test_post_operations_flow(base_url: str) -> None:

    post_data = {"title": "Flow Post", "body": "Flow content", "userId": 1}
    create_resp = requests.post(f"{base_url}/posts", json=post_data)
    assert create_resp.status_code == 201
    
    post_id = create_resp.json()['id']
    
    read_resp = requests.get(f"{base_url}/posts/{post_id}")
    assert read_resp.status_code == 200
    
    update_data = {"id": post_id, "title": "Updated", "body": "Updated", "userId": 2}
    update_resp = requests.put(f"{base_url}/posts/{post_id}", json=update_data)
    assert update_resp.status_code == 200
    
    delete_resp = requests.delete(f"{base_url}/posts/{post_id}")
    assert delete_resp.status_code == 200


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short"])