import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from api.main import app

client = TestClient(app)

def test_top_products_success(monkeypatch):
    # Mock get_top_products to return sample data
    sample = [{"product": "paracetamol", "mention_count": 5}]
    monkeypatch.setattr("medical_insights.src.api.crud.get_top_products", lambda limit=10: sample)
    response = client.get("/api/reports/top-products?limit=1")
    assert response.status_code == 200
    assert response.json() == sample

def test_top_products_not_found(monkeypatch):
    monkeypatch.setattr("medical_insights.src.api.crud.get_top_products", lambda limit=10: [])
    response = client.get("/api/reports/top-products?limit=1")
    assert response.status_code == 404

def test_channel_activity_daily_success(monkeypatch):
    sample = [{"date": "2024-06-01", "message_count": 3}]
    monkeypatch.setattr("medical_insights.src.api.crud.get_channel_activity", lambda channel, period: sample)
    response = client.get("/api/channels/test_channel/activity?period=daily")
    assert response.status_code == 200
    assert response.json() == sample

def test_channel_activity_weekly_success(monkeypatch):
    sample = [{"week": "2024-W22", "message_count": 10}]
    monkeypatch.setattr("medical_insights.src.api.crud.get_channel_activity", lambda channel, period: sample)
    response = client.get("/api/channels/test_channel/activity?period=weekly")
    assert response.status_code == 200
    assert response.json() == sample

def test_channel_activity_not_found(monkeypatch):
    monkeypatch.setattr("medical_insights.src.api.crud.get_channel_activity", lambda channel, period: [])
    response = client.get("/api/channels/test_channel/activity?period=daily")
    assert response.status_code == 404

def test_search_messages_success(monkeypatch):
    sample = [{"message_id": 1, "message_text": "paracetamol is available", "channel_sk": "abc123", "message_date": "2024-06-01T00:00:00"}]
    monkeypatch.setattr("medical_insights.src.api.crud.search_messages", lambda query: sample)
    response = client.get("/api/search/messages?query=paracetamol")
    assert response.status_code == 200
    assert response.json() == sample

def test_search_messages_not_found(monkeypatch):
    monkeypatch.setattr("medical_insights.src.api.crud.search_messages", lambda query: [])
    response = client.get("/api/search/messages?query=notfound")
    assert response.status_code == 404 