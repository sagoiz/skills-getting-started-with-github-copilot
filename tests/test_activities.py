"""Tests for activities endpoint"""
import pytest


def test_get_activities_success(client):
    """Test successful retrieval of all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_returns_correct_structure(client):
    """Test that activities have required fields"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity in data.items():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)


def test_get_activities_participants_are_emails(client):
    """Test that participants are stored as email strings"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity in data.items():
        for participant in activity["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant


def test_get_activities_has_all_expected_activities(client):
    """Test that all expected activities are present"""
    response = client.get("/activities")
    data = response.json()
    
    expected_activities = [
        "Chess Club",
        "Programming Class", 
        "Gym Class",
        "Basketball Team",
        "Soccer Club",
        "Art Club",
        "Drama Club",
        "Debate Club",
        "Science Club"
    ]
    
    for activity in expected_activities:
        assert activity in data