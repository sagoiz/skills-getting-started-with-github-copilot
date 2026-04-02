"""Tests for remove participant endpoint"""
import pytest


def test_remove_participant_success(client, sample_activity):
    """Test successful removal of a participant"""
    # Use an existing participant
    existing_email = "michael@mergington.edu"
    
    response = client.delete(
        f"/activities/{sample_activity}/participants/{existing_email}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert existing_email in data["message"]
    assert sample_activity in data["message"]


def test_remove_participant_removes_successfully(client, sample_activity):
    """Test that participant is actually removed"""
    existing_email = "michael@mergington.edu"
    
    # Check initial state
    response1 = client.get("/activities")
    assert existing_email in response1.json()[sample_activity]["participants"]
    
    # Remove participant
    client.delete(
        f"/activities/{sample_activity}/participants/{existing_email}"
    )
    
    # Verify removal
    response2 = client.get("/activities")
    assert existing_email not in response2.json()[sample_activity]["participants"]


def test_remove_participant_not_found(client, sample_activity):
    """Test removing participant that doesn't exist"""
    response = client.delete(
        f"/activities/{sample_activity}/participants/notexist@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_remove_from_nonexistent_activity(client):
    """Test removing from activity that doesn't exist"""
    response = client.delete(
        "/activities/Nonexistent Club/participants/test@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_remove_participant_twice(client, sample_activity):
    """Test removing the same participant twice"""
    existing_email = "daniel@mergington.edu"
    
    # First removal should succeed
    response1 = client.delete(
        f"/activities/{sample_activity}/participants/{existing_email}"
    )
    assert response1.status_code == 200
    
    # Second removal should fail
    response2 = client.delete(
        f"/activities/{sample_activity}/participants/{existing_email}"
    )
    assert response2.status_code == 404