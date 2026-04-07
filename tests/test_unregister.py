"""Test cases for DELETE /activities/{activity_name}/unregister endpoint using AAA pattern"""

import pytest


class TestUnregister:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_success_returns_200(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 200

    def test_unregister_success_removes_participant(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        # Act
        client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
        response = client.get("/activities")
        activities = response.json()
        # Assert
        chess_club = activities[activity_name]
        assert email not in chess_club["participants"]

    def test_unregister_success_response_message(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Unregistered {email} from {activity_name}" == data["message"]

    def test_unregister_not_signed_up_returns_400(self, client):
        # Arrange
        activity_name = "Basketball Team"
        email = "notsignedup@example.com"
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 400

    def test_unregister_not_signed_up_error_message(self, client):
        # Arrange
        activity_name = "Basketball Team"
        email = "notsignedup@example.com"
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Student is not signed up for this activity" == data["detail"]

    def test_unregister_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@example.com"
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 404

    def test_unregister_nonexistent_activity_error_message(self, client):
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@example.com"
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" == data["detail"]

    def test_unregister_preserves_other_participants(self, client):
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        email_to_keep = "daniel@mergington.edu"
        # Act
        client.delete(f"/activities/{activity_name}/unregister", params={"email": email_to_remove})
        response = client.get("/activities")
        activities = response.json()
        # Assert
        chess_club = activities[activity_name]
        assert email_to_remove not in chess_club["participants"]
        assert email_to_keep in chess_club["participants"]

    def test_unregister_re_signup_workflow(self, client):
        # Arrange
        activity_name = "Basketball Team"
        email = "test@example.com"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 200

    def test_unregister_case_sensitive_email(self, client):
        # Arrange
        activity_name = "Chess Club"
        email_lower = "michael@mergington.edu"
        email_upper = "MICHAEL@MERGINGTON.EDU"
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email_upper}
        )
        # Assert
        assert response.status_code == 400  # Case sensitive, so uppercase should fail