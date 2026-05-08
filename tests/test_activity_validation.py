import pytest

from src.app import activities


@pytest.mark.activities_signup
def test_duplicate_signup_does_not_change_participants(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    before_participants = list(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up"}
    assert activities[activity_name]["participants"] == before_participants


@pytest.mark.activities_unregister
def test_failed_unregister_keeps_participants_unchanged(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "missing.student@mergington.edu"
    before_participants = list(activities[activity_name]["participants"])

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": missing_email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}
    assert activities[activity_name]["participants"] == before_participants


@pytest.mark.activities_signup
def test_signup_adds_exactly_one_participant(client):
    # Arrange
    activity_name = "Robotics Club"
    student_email = "edge.case@mergington.edu"
    before_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})
    after_count = len(activities[activity_name]["participants"])

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {student_email} for {activity_name}"}
    assert after_count == before_count + 1


@pytest.mark.activities_get
def test_get_activities_structure_contains_required_fields(client):
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    for activity in payload.values():
        assert set(activity.keys()) == required_fields
