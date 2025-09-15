import pytest
from fastapi.testclient import TestClient
from app.crud.search import create_search_topic, create_search_details
from app.schemas.search import SearchTopicCreate, SearchDetailsCreate


class TestSearchTopics:
    """Test search topics endpoints"""
    
    def test_get_search_topics(self, client: TestClient, test_token):
        """Test getting all search topics"""
        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.get("/api/v1/search/topics", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_search_topic(self, client: TestClient, test_editor_token):
        """Test creating a search topic"""
        headers = {"Authorization": f"Bearer {test_editor_token}"}
        topic_data = {
            "title": "Test Topic",
            "popularity": 85.5,
            "ai_tips": "This is a test tip",
            "quick_actions": "Test action"
        }
        response = client.post("/api/v1/search/topics", json=topic_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Topic"
        assert data["popularity"] == 85.5
        assert "id" in data
    
    def test_create_search_topic_unauthorized(self, client: TestClient, test_token):
        """Test creating search topic without editor permissions"""
        headers = {"Authorization": f"Bearer {test_token}"}
        topic_data = {
            "title": "Test Topic",
            "popularity": 85.5,
            "ai_tips": "This is a test tip",
            "quick_actions": "Test action"
        }
        response = client.post("/api/v1/search/topics", json=topic_data, headers=headers)
        assert response.status_code == 403
    
    def test_get_search_topic_by_id(self, client: TestClient, test_token, session):
        """Test getting search topic by ID"""
        # Create a test topic first
        topic_data = SearchTopicCreate(
            title="Test Topic",
            popularity=85.5,
            ai_tips="This is a test tip",
            quick_actions="Test action"
        )
        topic = create_search_topic(session, topic_data)
        
        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.get(f"/api/v1/search/topics/{topic.id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Topic"
        assert data["id"] == topic.id
    
    def test_get_search_topic_not_found(self, client: TestClient, test_token):
        """Test getting non-existent search topic"""
        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.get("/api/v1/search/topics/99999", headers=headers)
        assert response.status_code == 404
    
    def test_update_search_topic(self, client: TestClient, test_editor_token, session):
        """Test updating search topic"""
        # Create a test topic first
        topic_data = SearchTopicCreate(
            title="Test Topic",
            popularity=85.5,
            ai_tips="This is a test tip",
            quick_actions="Test action"
        )
        topic = create_search_topic(session, topic_data)
        
        headers = {"Authorization": f"Bearer {test_editor_token}"}
        update_data = {
            "title": "Updated Topic",
            "popularity": 90.0
        }
        response = client.put(f"/api/v1/search/topics/{topic.id}", json=update_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Topic"
        assert data["popularity"] == 90.0
    
    def test_delete_search_topic(self, client: TestClient, test_admin_token, session):
        """Test deleting search topic"""
        # Create a test topic first
        topic_data = SearchTopicCreate(
            title="Test Topic",
            popularity=85.5,
            ai_tips="This is a test tip",
            quick_actions="Test action"
        )
        topic = create_search_topic(session, topic_data)
        
        headers = {"Authorization": f"Bearer {test_admin_token}"}
        response = client.delete(f"/api/v1/search/topics/{topic.id}", headers=headers)
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
    
    def test_search_topics_by_title(self, client: TestClient, test_token, session):
        """Test searching topics by title"""
        # Create test topics
        topic_data1 = SearchTopicCreate(title="Cooking Tips", popularity=85.5)
        topic_data2 = SearchTopicCreate(title="Cooking Recipes", popularity=90.0)
        create_search_topic(session, topic_data1)
        create_search_topic(session, topic_data2)
        
        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.get("/api/v1/search/topics/search?q=cooking", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all("cooking" in topic["title"].lower() for topic in data)


class TestSearchDetails:
    """Test search details endpoints"""
    
    def test_get_search_details(self, client: TestClient, test_token, session):
        """Test getting search details"""
        # Create a test topic and details
        topic_data = SearchTopicCreate(title="Test Topic", popularity=85.5)
        topic = create_search_topic(session, topic_data)
        
        details_data = SearchDetailsCreate(
            popularity_value=85.5,
            time_range="last 7 days",
            region="Global",
            suggested_title="Suggested Title",
            suggested_hashtags="#test #hashtag",
            suggested_script="This is a test script"
        )
        create_search_details(session, details_data, topic.id)
        
        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.get(f"/api/v1/search/details/{topic.id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["suggested_title"] == "Suggested Title"
        assert data["search_topic_id"] == topic.id
    
    def test_get_search_details_not_found(self, client: TestClient, test_token):
        """Test getting search details for non-existent topic"""
        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.get("/api/v1/search/details/99999", headers=headers)
        assert response.status_code == 404
    
    def test_create_search_details(self, client: TestClient, test_editor_token, session):
        """Test creating search details"""
        # Create a test topic first
        topic_data = SearchTopicCreate(title="Test Topic", popularity=85.5)
        topic = create_search_topic(session, topic_data)
        
        headers = {"Authorization": f"Bearer {test_editor_token}"}
        details_data = {
            "popularity_value": 85.5,
            "time_range": "last 7 days",
            "region": "Global",
            "suggested_title": "Suggested Title",
            "suggested_hashtags": "#test #hashtag",
            "suggested_script": "This is a test script"
        }
        response = client.post(f"/api/v1/search/details/{topic.id}", json=details_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["suggested_title"] == "Suggested Title"
        assert data["search_topic_id"] == topic.id
