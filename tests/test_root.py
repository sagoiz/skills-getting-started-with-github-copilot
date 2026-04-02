"""Tests for root endpoint"""
import pytest


def test_root_redirect(client):
    """Test that root endpoint redirects to /static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]


def test_root_redirect_follows(client):
    """Test that root redirect can be followed"""
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200