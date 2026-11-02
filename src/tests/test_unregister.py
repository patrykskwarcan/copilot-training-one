"""Unit tests for the POST /activities/{activity_name}/unregister endpoint."""

import pytest


class TestUnregister:
    """Test suite for POST /unregister endpoint."""

    def test_unregister_existing_student_success(self, fresh_app_client):
        """Test successfully unregistering a student from an activity."""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        
        response = fresh_app_client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        assert response.status_code == 200
        assert "message" in response.json()
        assert email in response.json()["message"]

    def test_unregister_removes_student_from_participants(self, fresh_app_client):
        """Test that unregister actually removes the student from the activity."""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        fresh_app_client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Verify the student is no longer in the activity
        response = fresh_app_client.get("/activities")
        activities = response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_response_message_format(self, fresh_app_client):
        """Test that the unregister response message has correct format."""
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        
        response = fresh_app_client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        message = response.json()["message"]
        assert "Unregistered" in message
        assert email in message
        assert activity_name in message

    def test_unregister_nonexistent_activity_404(self, fresh_app_client):
        """Test that unregistering from a non-existent activity returns 404."""
        response = fresh_app_client.post(
            "/activities/Nonexistent Club/unregister",
            params={"email": "student@mergington.edu"}
        )
        
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_student_not_signed_up_400(self, fresh_app_client):
        """Test that unregistering a student not in the activity returns 400."""
        activity_name = "Basketball Club"  # Empty by default
        email = "notregistered@mergington.edu"
        
        response = fresh_app_client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_from_empty_activity_400(self, fresh_app_client):
        """Test that unregistering from an empty activity returns 400."""
        activity_name = "Soccer Club"  # Empty by default
        email = "student@mergington.edu"
        
        response = fresh_app_client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_cannot_unregister_twice(self, fresh_app_client):
        """Test that unregistering twice fails on the second attempt."""
        activity_name = "Gym Class"
        email = "john@mergington.edu"  # Already in Gym Class
        
        # First unregister should succeed
        response1 = fresh_app_client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second unregister should fail
        response2 = fresh_app_client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        assert response2.status_code == 400
        assert "not signed up" in response2.json()["detail"]

    def test_unregister_one_student_leaves_others(self, fresh_app_client):
        """Test that unregistering one student doesn't affect others."""
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        email_to_keep = "daniel@mergington.edu"
        
        fresh_app_client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )
        
        # Verify the other student is still in the activity
        response = fresh_app_client.get("/activities")
        activities = response.json()
        assert email_to_remove not in activities[activity_name]["participants"]
        assert email_to_keep in activities[activity_name]["participants"]

    def test_unregister_then_signup_again(self, fresh_app_client):
        """Test that a student can unregister and then sign up again."""
        activity_name = "Art Club"
        email = "student@mergington.edu"
        
        # Signup first time
        response1 = fresh_app_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Unregister
        response2 = fresh_app_client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Sign up again
        response3 = fresh_app_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response3.status_code == 200
        
        # Verify student is in the activity
        response = fresh_app_client.get("/activities")
        activities = response.json()
        assert email in activities[activity_name]["participants"]

    def test_unregister_empty_email(self, fresh_app_client):
        """Test that unregister with empty email is handled."""
        activity_name = "Drama Club"
        response = fresh_app_client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": ""}
        )
        
        # Empty email should either be rejected or handled gracefully
        # For now, we just verify the behavior is consistent
        assert response.status_code in [200, 400]

    def test_unregister_activity_name_case_sensitivity(self, fresh_app_client):
        """Test that activity names are case-sensitive in unregister."""
        response = fresh_app_client.post(
            "/activities/chess club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        
        # Should fail because "chess club" != "Chess Club"
        assert response.status_code == 404

    def test_unregister_participant_count_decreases(self, fresh_app_client):
        """Test that participant count decreases after unregister."""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Get initial count
        response = fresh_app_client.get("/activities")
        initial_count = len(response.json()[activity_name]["participants"])
        
        # Unregister
        fresh_app_client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Get updated count
        response = fresh_app_client.get("/activities")
        updated_count = len(response.json()[activity_name]["participants"])
        
        assert updated_count == initial_count - 1

    def test_unregister_special_characters_in_email(self, fresh_app_client):
        """Test unregister with special characters in email."""
        activity_name = "Debate Club"
        email = "student+tag@mergington.edu"
        
        # First signup with special characters
        fresh_app_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Then unregister
        response = fresh_app_client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Should succeed
        assert response.status_code == 200
        
        # Verify student is no longer in the activity
        response = fresh_app_client.get("/activities")
        activities = response.json()
        assert email not in activities[activity_name]["participants"]
