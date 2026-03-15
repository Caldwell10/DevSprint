import uuid

import pytest


@pytest.mark.asyncio
async def test_create_session_success(client):
    payload = {
        "session_type": "coding",
        "duration_minutes": 45,
        "topic": "FastAPI testing",
        "notes": "wrote initial endpoint tests",
    }

    response = await client.post("/api/v1/sessions/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["session_type"] == payload["session_type"]
    assert data["duration_minutes"] == payload["duration_minutes"]
    assert data["topic"] == payload["topic"]
    assert data["notes"] == payload["notes"]

    
    uuid.UUID(data["id"])
    assert data["created_at"]


@pytest.mark.asyncio
async def test_create_session_invalid_type(client):
    payload = {
        "session_type": "gaming",
        "duration_minutes": 30,
        "topic": "not allowed type",
    }

    response = await client.post("/api/v1/sessions/", json=payload)

    assert response.status_code == 422
    body = response.json()
    assert any("session_type" in str(err.get("loc", [])) for err in body.get("detail", []))


@pytest.mark.asyncio
async def test_create_session_invalid_duration(client):
    payload = {
        "session_type": "study",
        "duration_minutes": 0,
        "topic": "duration must be positive",
    }

    response = await client.post("/api/v1/sessions/", json=payload)

    assert response.status_code == 422
    body = response.json()
    assert any("duration_minutes" in str(err.get("loc", [])) for err in body.get("detail", []))


@pytest.mark.asyncio
async def test_list_sessions_order_desc(client):
    first = {
        "session_type": "study",
        "duration_minutes": 25,
        "topic": "morning review",
    }
    second = {
        "session_type": "leetcode",
        "duration_minutes": 40,
        "topic": "graphs practice",
    }

    res1 = await client.post("/api/v1/sessions/", json=first)
    res2 = await client.post("/api/v1/sessions/", json=second)

    assert res1.status_code == 201
    assert res2.status_code == 201

    list_res = await client.get("/api/v1/sessions/")
    assert list_res.status_code == 200

    items = list_res.json()
    assert len(items) == 2
    assert items[0]["id"] == res2.json()["id"]
    assert items[1]["id"] == res1.json()["id"]
