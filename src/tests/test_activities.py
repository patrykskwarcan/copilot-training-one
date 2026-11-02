"""Unit tests for the GET /activities endpoint and root endpoint."""

import pytest


class TestRootEndpoint:
    """Test suite for the root GET / endpoint."""

    def test_root_redirects_to_static_index(self, client):
        """Test that root endpoint redirects to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns status 200."""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary."""
        response = client.get("/activities")
        assert isinstance(response.json(), dict)

    def test_get_activities_has_all_activities(self, client):
        """Test that all 9 expected activities are present."""
        response = client.get("/activities")
        activities = response.json()
        
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Club",
            "Soccer Club",
            "Art Club",
            "Drama Club",
            "Debate Club",
            "Science Club"
        ]
        
        for activity in expected_activities:
            assert activity in activities

    def test_activity_has_required_fields(self, client):
        """Test that each activity has all required fields."""
        response = client.get("/activities")
        activities = response.json()
        
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(activity_data.keys()), \
                f"Activity '{activity_name}' missing required fields"

    def test_activity_description_is_string(self, client):
        """Test that each activity's description is a string."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["description"], str), \
                f"Activity '{activity_name}' description is not a string"
            assert len(activity_data["description"]) > 0, \
                f"Activity '{activity_name}' description is empty"

    def test_activity_schedule_is_string(self, client):
        """Test that each activity's schedule is a string."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["schedule"], str), \
                f"Activity '{activity_name}' schedule is not a string"
            assert len(activity_data["schedule"]) > 0, \
                f"Activity '{activity_name}' schedule is empty"

    def test_max_participants_is_integer(self, client):
        """Test that max_participants is a positive integer."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"Activity '{activity_name}' max_participants is not an integer"
            assert activity_data["max_participants"] > 0, \
                f"Activity '{activity_name}' max_participants is not positive"

    def test_participants_is_list(self, client):
        """Test that participants is a list."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"Activity '{activity_name}' participants is not a list"

    def test_participants_are_strings(self, client):
        """Test that all participants are strings (emails)."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str), \
                    f"Activity '{activity_name}' has non-string participant"

    def test_initial_participants_count(self, client):
        """Test that initial participant counts are as expected."""
        response = client.get("/activities")
        activities = response.json()
        
        # Some activities should have initial participants
        assert len(activities["Chess Club"]["participants"]) == 2
        assert len(activities["Programming Class"]["participants"]) == 2
        assert len(activities["Gym Class"]["participants"]) == 2
        
        # Some activities should start empty
        assert len(activities["Basketball Club"]["participants"]) == 0
        assert len(activities["Soccer Club"]["participants"]) == 0
