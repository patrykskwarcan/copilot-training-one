"""Shared pytest fixtures for FastAPI tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def fresh_app_client():
    """
    Provide a TestClient with a fresh app state.
    This resets the activities data before each test.
    """
    from src.app import app, activities
    
    # Define the original activities state
    original_activities = {
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
        "Basketball Club": {
            "description": "Practice basketball skills and play team games",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Soccer Club": {
            "description": "Develop soccer skills and compete in friendly matches",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 22,
            "participants": []
        },
        "Art Club": {
            "description": "Explore drawing, painting, and other visual arts",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": []
        },
        "Drama Club": {
            "description": "Practice acting and collaborate on theatrical productions",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Debate Club": {
            "description": "Build public speaking skills and discuss important topics",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": []
        },
        "Science Club": {
            "description": "Explore scientific ideas through experiments and projects",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": []
        }
    }
    
    # Reset activities to original state before each test
    activities.clear()
    for key, value in original_activities.items():
        activities[key] = value.copy()
        activities[key]["participants"] = value["participants"].copy()
    
    client = TestClient(app)
    yield client
    
    # Cleanup: restore original state after test
    activities.clear()
    for key, value in original_activities.items():
        activities[key] = value.copy()
        activities[key]["participants"] = value["participants"].copy()


@pytest.fixture
def sample_email():
    """Provide a sample student email for testing."""
    return "test@mergington.edu"


@pytest.fixture
def sample_activity_name():
    """Provide a sample activity name for testing."""
    return "Chess Club"
