def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_adds_participant(client):
    response = client.post(
        "/activities/Chess%20Club/signup?email=test%40example.com"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up test@example.com for Chess Club"

    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"]
    assert "test@example.com" in participants


def test_signup_duplicate_returns_400(client):
    first_response = client.post(
        "/activities/Chess%20Club/signup?email=test%40example.com"
    )
    assert first_response.status_code == 200

    duplicate_response = client.post(
        "/activities/Chess%20Club/signup?email=test%40example.com"
    )

    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student already signed up"


def test_remove_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/participants?email=michael%40mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"]
    assert "michael@mergington.edu" not in participants


def test_remove_missing_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/participants?email=missing%40example.com"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
