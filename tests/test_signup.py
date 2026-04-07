"""Test cases for POST /activities/{activity_name}/signup endpoint using AAA pattern"""

import pytest


class TestSignup:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success_returns_200(self, client):
        # Arrange
        activity_name = "Basketball Team"
        email = "test@example.com"
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 200

    def test_signup_success_adds_participant(self, client):
        # Arrange
        activity_name = "Basketball Team"
        email = "test@example.com"
        # Act
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        response = client.get("/activities")
        activities = response.json()
        # Assert
        basketball_team = activities[activity_name]
        assert email in basketball_team["participants"]

    def test_signup_success_response_message(self, client):
        # Arrange
        activity_name = "Basketball Team"
        email = "test@example.com"
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Signed up {email} for {activity_name}" == data["message"]

    def test_signup_duplicate_email_returns_400(self, client):
        # Arrange
        activity_name = "Basketball Team"
        email = "test@example.com"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 400

    def test_signup_duplicate_email_error_message(self, client):
        # Arrange
        activity_name = "Basketball Team"
        email = "test@example.com"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Student already signed up for this activity" == data["detail"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@example.com"
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 404

    def test_signup_nonexistent_activity_error_message(self, client):
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@example.com"
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" == data["detail"]

    def test_signup_multiple_activities_same_email(self, client):
        # Arrange
        email = "test@example.com"
        activity1 = "Basketball Team"
        activity2 = "Soccer Club"
        # Act
        response1 = client.post(f"/activities/{activity1}/signup", params={"email": email})
        response2 = client.post(f"/activities/{activity2}/signup", params={"email": email})
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_signup_preserves_existing_participants(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@example.com"
        # Act
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        response = client.get("/activities")
        activities = response.json()
        # Assert
        chess_club = activities[activity_name]
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
        assert email in chess_club["participants"]