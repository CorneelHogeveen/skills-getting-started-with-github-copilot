"""
Tests for GET /activities endpoint.

Tests the retrieval of all extracurricular activities available at Mergington High School.
Uses AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_returns_200(self, client):
        """
        Act: Send GET request to /activities
        Assert: Response status code is 200
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client, sample_activities):
        """
        Arrange: Know that 9 activities are defined in the app
        Act: Send GET request to /activities
        Assert: Response contains all 9 activities
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert len(data) == 9
        assert set(data.keys()) == set(sample_activities.keys())

    def test_get_activities_returns_correct_activity_names(self, client):
        """
        Act: Send GET request to /activities
        Assert: Response contains expected activity names
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Theater Club",
            "Debate Team",
            "Science Club"
        ]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert sorted(data.keys()) == sorted(expected_activities)

    def test_get_activities_returns_activity_with_required_fields(self, client):
        """
        Arrange: Know that each activity must have required fields
        Act: Send GET request to /activities
        Assert: Each activity contains all required fields
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data, dict), f"{activity_name} is not a dict"
            assert set(activity_data.keys()) == required_fields, \
                f"{activity_name} missing or has extra fields"

    def test_get_activities_participants_is_list(self, client):
        """
        Arrange: Know that participants field must be a list
        Act: Send GET request to /activities
        Assert: Participants field is a list for each activity
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list), \
                f"{activity_name} participants is not a list"

    def test_get_activities_returns_correct_schedule_format(self, client):
        """
        Arrange: Know that schedule is a string
        Act: Send GET request to /activities
        Assert: Schedule field is a string for each activity
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["schedule"], str), \
                f"{activity_name} schedule is not a string"
            assert len(activity_data["schedule"]) > 0, \
                f"{activity_name} schedule is empty"

    def test_get_activities_has_valid_max_participants(self, client):
        """
        Arrange: Know that max_participants must be a positive integer
        Act: Send GET request to /activities
        Assert: Max_participants is a positive integer for each activity
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            max_part = activity_data["max_participants"]
            assert isinstance(max_part, int), \
                f"{activity_name} max_participants is not an int"
            assert max_part > 0, \
                f"{activity_name} max_participants must be positive"

    def test_get_activities_chess_club_has_initial_participants(self, client):
        """
        Arrange: Know Chess Club has initial participants
        Act: Send GET request to /activities
        Assert: Chess Club participants list contains expected members
        """
        # Arrange
        expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert data["Chess Club"]["participants"] == expected_participants

    def test_get_activities_response_is_json(self, client):
        """
        Act: Send GET request to /activities
        Assert: Response content type is application/json
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.headers["content-type"] == "application/json"

    def test_get_activities_description_not_empty(self, client):
        """
        Arrange: Know that all activities must have non-empty descriptions
        Act: Send GET request to /activities
        Assert: Description field is non-empty for each activity
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            description = activity_data["description"]
            assert isinstance(description, str), \
                f"{activity_name} description is not a string"
            assert len(description) > 0, \
                f"{activity_name} description is empty"
