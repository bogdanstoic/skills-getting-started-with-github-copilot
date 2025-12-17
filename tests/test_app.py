from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success():
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    assert "Signed up test@example.com for Chess Club" == response.json()["message"]


def test_signup_already_signed():
    # First signup
    client.post("/activities/Basketball/signup?email=test2@example.com")
    # Second attempt
    response = client.post("/activities/Basketball/signup?email=test2@example.com")
    assert response.status_code == 400
    assert "Student already signed up for this activity" == response.json()["detail"]


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=test@example.com")
    assert response.status_code == 404
    assert "Activity not found" == response.json()["detail"]


def test_delete_success():
    # First signup
    client.post("/activities/Tennis/signup?email=test3@example.com")
    # Then delete
    response = client.delete("/activities/Tennis/signup?email=test3@example.com")
    assert response.status_code == 200
    assert "Unregistered test3@example.com from Tennis" == response.json()["message"]


def test_delete_not_signed():
    response = client.delete("/activities/Chess%20Club/signup?email=notsigned@example.com")
    assert response.status_code == 400
    assert "Student not signed up for this activity" == response.json()["detail"]


def test_delete_activity_not_found():
    response = client.delete("/activities/Nonexistent/signup?email=test@example.com")
    assert response.status_code == 404
    assert "Activity not found" == response.json()["detail"]