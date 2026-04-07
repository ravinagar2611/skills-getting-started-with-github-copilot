"""Pytest configuration and fixtures for API tests"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provides a test client for API endpoints."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture to reset activities to initial state before and after each test.
    
    This ensures test isolation by providing a clean slate for each test case.
    """
    # Store the initial state
    initial_activities = deepcopy(activities)
    
    # Reset activities to initial state
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Practice and compete in basketball games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": []
        },
        "Soccer Club": {
            "description": "Train for soccer matches and improve skills",
            "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
            "max_participants": 20,
            "participants": []
        },
        "Art Club": {
            "description": "Explore painting, drawing, and creative arts",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": []
        },
        "Drama Club": {
            "description": "Act in plays and learn theater skills",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Debate Club": {
            "description": "Practice public speaking and argumentation",
            "schedule": "Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 12,
            "participants": []
        },
        "Science Club": {
            "description": "Conduct experiments and learn about science",
            "schedule": "Tuesdays, 4:00 PM - 5:00 PM",
            "max_participants": 18,
            "participants": []
        }
    })
    
    yield
    
    # Reset after test
    activities.clear()
    activities.update(initial_activities)