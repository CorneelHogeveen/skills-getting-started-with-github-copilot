"""
Tests for GET / endpoint.

Tests the root redirect functionality that directs users to the web interface.
Uses AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


class TestRootRedirect:
    """Test suite for GET / endpoint."""

    def test_root_returns_redirect(self, client):
        """
        Act: Send GET request to root path /
        Assert: Response is a redirect (3xx status code)
        """
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code in [301, 302, 303, 307, 308]

    def test_root_redirects_to_static_index(self, client):
        """
        Act: Send GET request to root path /
        Assert: Redirect location is /static/index.html
        """
        # Arrange
        expected_location = "/static/index.html"
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert "location" in response.headers
        assert response.headers["location"] == expected_location

    def test_root_redirect_status_307(self, client):
        """
        Act: Send GET request to root path /
        Assert: Response status code is 307 (Temporary Redirect)
        """
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307

    def test_root_with_follow_redirects_reaches_static(self, client):
        """
        Act: Send GET request to root path / following redirects
        Assert: Final response is from static files (200 or 404 if file missing)
        """
        # Act
        response = client.get("/", follow_redirects=True)
        
        # Assert - Should either find the file (200) or not (404)
        # Both are acceptable as we're testing the redirect works, not if index.html exists
        assert response.status_code in [200, 404]

    def test_root_response_headers_contain_location(self, client):
        """
        Arrange: Know that redirects require a Location header
        Act: Send GET request to root path /
        Assert: Response includes Location header
        """
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert "location" in response.headers
        assert len(response.headers["location"]) > 0

    def test_root_redirect_uses_relative_path(self, client):
        """
        Act: Send GET request to root path /
        Assert: Redirect location uses relative path (not absolute URL)
        """
        # Act
        response = client.get("/", follow_redirects=False)
        location = response.headers["location"]
        
        # Assert
        # Relative paths start with / and don't contain protocol
        assert location.startswith("/")
        assert "http://" not in location
        assert "https://" not in location

    def test_root_no_body_on_redirect(self, client):
        """
        Arrange: Know that redirect responses typically have minimal body
        Act: Send GET request to root path /
        Assert: Response body is minimal (empty or small)
        """
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        # Redirects typically have empty or minimal body
        assert len(response.text) < 100  # Typical redirect response is very small

    def test_root_accepts_get_method(self, client):
        """
        Act: Send GET request to root path /
        Assert: GET method is accepted (returns 2xx or 3xx, not 405)
        """
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code != 405  # Method Not Allowed

    def test_root_multiple_requests_consistent_redirect(self, client):
        """
        Arrange: Make multiple requests to root path
        Act: Send multiple GET requests to /
        Assert: All requests redirect to same location
        """
        # Arrange
        expected_location = "/static/index.html"
        
        # Act & Assert
        for _ in range(3):
            response = client.get("/", follow_redirects=False)
            assert response.status_code == 307
            assert response.headers["location"] == expected_location

    def test_root_redirect_location_case_sensitive(self, client):
        """
        Act: Send GET request to root path /
        Assert: Redirect location matches exact case
        """
        # Act
        response = client.get("/", follow_redirects=False)
        location = response.headers["location"]
        
        # Assert
        # Verify the exact path is returned
        assert location == "/static/index.html"
        assert location != "/Static/index.html"
        assert location != "/static/Index.html"
