"""Test cases for GET /activities endpoint using AAA pattern"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_returns_200_status(self, client):
        # Arrange - no setup needed
        # Act
        response = client.get("/activities")
        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_list(self, client):
        # Arrange - no setup needed
        # Act
        response = client.get("/activities")
        # Assert
        assert isinstance(response.json(), dict)

    def test_get_activities_has_required_fields(self, client):
        # Arrange - no setup needed
        required_fields = ["description", "schedule", "max_participants", "participants"]
        # Act
        response = client.get("/activities")
        activities = response.json()
        # Assert
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data

    def test_get_activities_participants_is_list(self, client):
        # Arrange - no setup needed
        # Act
        response = client.get("/activities")
        activities = response.json()
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_max_participants_is_integer(self, client):
        # Arrange - no setup needed
        # Act
        response = client.get("/activities")
        activities = response.json()
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0

    def test_get_activities_preserves_initial_participants(self, client):
        # Arrange - no setup needed
        # Act
        response = client.get("/activities")
        activities = response.json()
        # Assert
        chess_club = activities["Chess Club"]
        programming_class = activities["Programming Class"]
        gym_class = activities["Gym Class"]

        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
        assert "emma@mergington.edu" in programming_class["participants"]
        assert "sophia@mergington.edu" in programming_class["participants"]
        assert "john@mergington.edu" in gym_class["participants"]
        assert "olivia@mergington.edu" in gym_class["participants"]