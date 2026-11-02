"""Unit tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignup:
    """Test suite for POST /signup endpoint."""

    def test_signup_new_student_success(self, fresh_app_client, sample_email):
        """Test successfully signing up a new student for an activity."""
        activity_name = "Basketball Club"
        response = fresh_app_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        
        assert response.status_code == 200
        assert "message" in response.json()
        assert sample_email in response.json()["message"]

    def test_signup_adds_student_to_participants(self, fresh_app_client, sample_email):
        """Test that signup actually adds the student to the activity."""
        activity_name = "Basketball Club"
        fresh_app_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        
        # Verify the student is now in the activity
        response = fresh_app_client.get("/activities")
        activities = response.json()
        assert sample_email in activities[activity_name]["participants"]

    def test_signup_response_message_format(self, fresh_app_client, sample_email):
        """Test that the signup response message has correct format."""
        activity_name = "Soccer Club"
        response = fresh_app_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        
        message = response.json()["message"]
        assert "Signed up" in message
        assert sample_email in message
        assert activity_name in message

    def test_signup_nonexistent_activity_404(self, fresh_app_client, sample_email):
        """Test that signing up for a non-existent activity returns 404."""
        response = fresh_app_client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": sample_email}
        )
        
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_student_400(self, fresh_app_client, sample_email):
        """Test that duplicate signup returns 400 error."""
        activity_name = "Chess Club"
        
        # First signup should succeed
        response1 = fresh_app_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        assert response1.status_code == 200
        
        # Duplicate signup should fail
        response2 = fresh_app_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"]

    def test_signup_already_signed_up_student(self, fresh_app_client):
        """Test that a student already in an activity can't sign up again."""
        activity_name = "Chess Club"
        # michael@mergington.edu is already in Chess Club
        existing_email = "michael@mergington.edu"
        
        response = fresh_app_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_multiple_students_same_activity(self, fresh_app_client):
        """Test that multiple different students can sign up for the same activity."""
        activity_name = "Art Club"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        response1 = fresh_app_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        assert response1.status_code == 200
        
        response2 = fresh_app_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        assert response2.status_code == 200
        
        # Verify both are in the activity
        response = fresh_app_client.get("/activities")
        activities = response.json()
        assert email1 in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]

    def test_signup_same_student_different_activities(self, fresh_app_client, sample_email):
        """Test that same student can sign up for multiple different activities."""
        activity1 = "Drama Club"
        activity2 = "Debate Club"
        
        response1 = fresh_app_client.post(
            f"/activities/{activity1}/signup",
            params={"email": sample_email}
        )
        assert response1.status_code == 200
        
        response2 = fresh_app_client.post(
            f"/activities/{activity2}/signup",
            params={"email": sample_email}
        )
        assert response2.status_code == 200
        
        # Verify student is in both activities
        response = fresh_app_client.get("/activities")
        activities = response.json()
        assert sample_email in activities[activity1]["participants"]
        assert sample_email in activities[activity2]["participants"]

    def test_signup_empty_email(self, fresh_app_client):
        """Test that signup with empty email is handled."""
        activity_name = "Gym Class"
        response = fresh_app_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": ""}
        )
        
        # Empty email should either be rejected or treated as a valid (but unusual) email
        # For now, we just verify the behavior is consistent
        assert response.status_code in [200, 400]

    def test_signup_activity_name_case_sensitivity(self, fresh_app_client, sample_email):
        """Test that activity names are case-sensitive."""
        response = fresh_app_client.post(
            "/activities/chess club/signup",
            params={"email": sample_email}
        )
        
        # Should fail because "chess club" != "Chess Club"
        assert response.status_code == 404

    def test_signup_special_characters_in_email(self, fresh_app_client):
        """Test signup with special characters in email."""
        activity_name = "Science Club"
        email = "student+tag@mergington.edu"
        
        response = fresh_app_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Should succeed as it's a valid email format
        assert response.status_code == 200
        
        # Verify the email is stored correctly
        response = fresh_app_client.get("/activities")
        activities = response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_participant_count_increases(self, fresh_app_client):
        """Test that participant count increases after each signup."""
        activity_name = "Basketball Club"
        
        # Get initial count
        response = fresh_app_client.get("/activities")
        initial_count = len(response.json()[activity_name]["participants"])
        
        # Signup a new student
        fresh_app_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        
        # Get updated count
        response = fresh_app_client.get("/activities")
        updated_count = len(response.json()[activity_name]["participants"])
        
        assert updated_count == initial_count + 1
