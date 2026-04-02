"""Integration tests for the activities API"""
import pytest


def test_complete_signup_flow(client):
    """Test complete flow: get activities -> signup -> verify"""
    # Step 1: Get activities
    response = client.get("/activities")
    assert response.status_code == 200
    activities_data = response.json()
    
    # Step 2: Signup for an activity
    activity = "Chess Club"
    email = "integration@test.edu"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Step 3: Verify signup
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]


def test_complete_removal_flow(client):
    """Test complete flow: get activities -> verify participant -> remove -> verify"""
    activity = "Chess Club"
    email = "michael@mergington.edu"
    
    # Step 1: Verify participant exists
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]
    
    # Step 2: Remove participant
    response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )
    assert response.status_code == 200
    
    # Step 3: Verify removal
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]


def test_error_handling_flow(client):
    """Test various error conditions"""
    # Non-existent activity
    response = client.post("/activities/Fake Club/signup", params={"email": "test@test.edu"})
    assert response.status_code == 404
    
    # Missing email parameter
    response = client.post("/activities/Chess Club/signup")
    assert response.status_code == 422
    
    # Duplicate signup
    email = "michael@mergington.edu"
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response.status_code == 400


def test_response_format_consistency(client):
    """Test that all responses follow consistent format"""
    # Test GET response
    response = client.get("/activities")
    assert response.headers["content-type"].startswith("application/json")
    
    # Test POST response
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "test@mergington.edu"}
    )
    assert response.headers["content-type"].startswith("application/json")
    assert isinstance(response.json(), dict)
    
    # Test DELETE response
    response = client.delete(
        "/activities/Art Club/participants/ava@mergington.edu"
    )
    assert response.headers["content-type"].startswith("application/json")