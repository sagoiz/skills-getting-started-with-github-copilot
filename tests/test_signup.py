"""Tests for signup endpoint"""
import pytest


def test_signup_success(client, sample_activity, new_email):
    """Test successful signup for an activity"""
    response = client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": new_email}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert new_email in data["message"]
    assert sample_activity in data["message"]


def test_signup_adds_participant(client, sample_activity, new_email):
    """Test that signup actually adds the participant"""
    # First get current participants
    response1 = client.get("/activities")
    initial_count = len(response1.json()[sample_activity]["participants"])
    
    # Signup new participant
    client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": new_email}
    )
    
    # Check participant was added
    response2 = client.get("/activities")
    final_count = len(response2.json()[sample_activity]["participants"])
    assert final_count == initial_count + 1
    assert new_email in response2.json()[sample_activity]["participants"]


def test_signup_activity_not_found(client, new_email):
    """Test signup to non-existent activity"""
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": new_email}
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_already_signed_up(client, sample_activity, sample_email):
    """Test signup when student is already signed up"""
    response = client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": sample_email}
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_multiple_activities(client, new_email):
    """Test that a student can sign up for multiple activities"""
    activities = ["Chess Club", "Programming Class"]
    
    for activity in activities:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": new_email}
        )
        assert response.status_code == 200
    
    # Verify both signups succeeded
    response = client.get("/activities")
    data = response.json()
    assert new_email in data[activities[0]]["participants"]
    assert new_email in data[activities[1]]["participants"]


def test_signup_email_parameter(client, sample_activity):
    """Test that email parameter is required"""
    response = client.post(f"/activities/{sample_activity}/signup")
    # FastAPI should return 422 for missing required parameter
    assert response.status_code == 422