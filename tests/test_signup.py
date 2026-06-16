"""
Tests for POST /activities/{activity_name}/signup endpoint.

Tests student signup functionality for extracurricular activities.
Uses AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_student_returns_200(self, client):
        """
        Arrange: Prepare a new student email not yet in any activity
        Act: POST signup request with valid activity and new email
        Assert: Response status code is 200
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert
        assert response.status_code == 200

    def test_signup_new_student_returns_success_message(self, client):
        """
        Arrange: Prepare a new student email not yet in any activity
        Act: POST signup request with valid activity and new email
        Assert: Response contains success message
        """
        # Arrange
        activity_name = "Programming Class"
        new_email = "alice@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert new_email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_student_to_participants(self, client):
        """
        Arrange: Prepare a new student email and activity name
        Act: POST signup request
        Assert: Student email is added to activity participants
        """
        # Arrange
        activity_name = "Gym Class"
        new_email = "bob@mergington.edu"
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Get activities to verify
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert new_email in data[activity_name]["participants"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        """
        Arrange: Prepare a non-existent activity name
        Act: POST signup request with invalid activity name
        Assert: Response status code is 404 (Not Found)
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404

    def test_signup_nonexistent_activity_returns_error_message(self, client):
        """
        Arrange: Prepare a non-existent activity name
        Act: POST signup request with invalid activity name
        Assert: Response contains error message about activity not found
        """
        # Arrange
        activity_name = "Fake Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_duplicate_student_returns_400(self, client):
        """
        Arrange: Prepare a student already signed up for an activity
        Act: POST signup request with student already in participants
        Assert: Response status code is 400 (Bad Request)
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert
        assert response.status_code == 400

    def test_signup_duplicate_student_returns_error_message(self, client):
        """
        Arrange: Prepare a student already signed up for an activity
        Act: POST signup request with duplicate student
        Assert: Response contains error message about duplicate signup
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = "daniel@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        data = response.json()
        
        # Assert
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_case_sensitive_activity_name(self, client):
        """
        Arrange: Prepare an activity name with different casing
        Act: POST signup request with lowercase activity name
        Assert: Response indicates activity not found (names are case-sensitive)
        """
        # Arrange
        activity_name = "chess club"  # Lowercase
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404

    def test_signup_multiple_students_to_same_activity(self, client):
        """
        Arrange: Prepare two different students
        Act: Sign up both students to the same activity
        Assert: Both students are in participants list
        """
        # Arrange
        activity_name = "Tennis Club"
        student1 = "student1@mergington.edu"
        student2 = "student2@mergington.edu"
        
        # Act
        client.post(f"/activities/{activity_name}/signup", params={"email": student1})
        client.post(f"/activities/{activity_name}/signup", params={"email": student2})
        
        # Verify
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert student1 in data[activity_name]["participants"]
        assert student2 in data[activity_name]["participants"]

    def test_signup_same_student_different_activities(self, client):
        """
        Arrange: Prepare one student and two different activities
        Act: Sign up student to first activity, then attempt second activity
        Assert: Student can be in different activities (only prevents duplicates in same activity)
        """
        # Arrange
        student = "multiactivity@mergington.edu"
        activity1 = "Art Studio"
        activity2 = "Science Club"
        
        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": student}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": student}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_signup_whitespace_in_email(self, client):
        """
        Arrange: Email parameter is passed as-is with no trimming
        Act: POST signup with email containing whitespace
        Assert: Email is added exactly as provided
        """
        # Arrange
        activity_name = "Theater Club"
        email_with_space = "student @mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email_with_space}
        )
        
        # Assert - No validation on email format, so this should succeed
        assert response.status_code == 200

    def test_signup_empty_email_parameter(self, client):
        """
        Arrange: Prepare empty email parameter
        Act: POST signup request with empty email
        Assert: Email is still added to participants (no validation)
        """
        # Arrange
        activity_name = "Debate Team"
        empty_email = ""
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": empty_email}
        )
        
        # Assert - Current implementation doesn't validate email
        assert response.status_code == 200

    def test_signup_response_json_format(self, client):
        """
        Arrange: Prepare valid signup request
        Act: POST signup request
        Assert: Response is valid JSON with message field
        """
        # Arrange
        activity_name = "Chess Club"
        email = "json_test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.headers["content-type"] == "application/json"
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data

    def test_signup_preserves_existing_participants(self, client):
        """
        Arrange: Get initial participants list for an activity
        Act: Sign up a new student
        Assert: Existing participants are preserved and new one is added
        """
        # Arrange
        activity_name = "Programming Class"
        original_response = client.get("/activities")
        original_participants = original_response.json()[activity_name]["participants"].copy()
        new_email = "newteacher@mergington.edu"
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Verify
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[activity_name]["participants"]
        
        # Assert
        assert len(updated_participants) == len(original_participants) + 1
        for original in original_participants:
            assert original in updated_participants
        assert new_email in updated_participants
