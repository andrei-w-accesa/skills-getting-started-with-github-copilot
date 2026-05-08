import pytest


@pytest.mark.activities_get
def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_keys = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Debate Team",
        "Robotics Club",
        "Drama Club",
        "Art Studio",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == expected_keys


@pytest.mark.activities_signup
def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    student_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {student_email} for {activity_name}"}
    updated_activity = activities_response.json()[activity_name]
    assert student_email in updated_activity["participants"]


@pytest.mark.activities_signup
def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    student_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


@pytest.mark.activities_signup
def test_signup_returns_bad_request_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up"}


@pytest.mark.activities_unregister
def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": existing_email}
    )
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {existing_email} from {activity_name}"
    }
    updated_activity = activities_response.json()[activity_name]
    assert existing_email not in updated_activity["participants"]


@pytest.mark.activities_unregister
def test_unregister_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    student_email = "new.student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": student_email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


@pytest.mark.activities_unregister
def test_unregister_returns_not_found_for_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "missing.student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": missing_email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}
