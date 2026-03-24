import pytest


class TestRoot:
    def test_root_redirects_to_static(self, client):
        # Arrange: No special setup needed

        # Act: Make GET request to root without following redirects
        response = client.get("/", follow_redirects=False)

        # Assert: Should return redirect status and correct location
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"


class TestGetActivities:
    def test_get_all_activities_returns_dict(self, client):
        # Arrange: No special setup needed

        # Act: Make GET request to activities
        response = client.get("/activities")

        # Assert: Should return 200 and dict
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_get_activities_contains_expected_keys(self, client):
        # Arrange: No special setup needed

        # Act: Make GET request to activities
        response = client.get("/activities")

        # Assert: Should contain expected activity keys
        data = response.json()
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class",
            "Basketball Team", "Tennis Club", "Drama Club",
            "Art Studio", "Debate Team", "Science Club"
        ]
        assert set(data.keys()) == set(expected_activities)

    def test_activities_structure_valid(self, client):
        # Arrange: No special setup needed

        # Act: Make GET request to activities
        response = client.get("/activities")

        # Assert: Each activity should have required fields
        data = response.json()
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignupForActivity:
    def test_signup_success(self, client, sample_email):
        # Arrange: Choose an activity and email
        activity_name = "Chess Club"

        # Act: Make POST request to signup
        response = client.post(f"/activities/{activity_name}/signup?email={sample_email}")

        # Assert: Should return 200 and success message
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]

        # Assert: Participant should be added to activity
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert sample_email in activities[activity_name]["participants"]

    def test_signup_duplicate_email_fails(self, client, sample_email):
        # Arrange: Sign up first
        activity_name = "Programming Class"
        client.post(f"/activities/{activity_name}/signup?email={sample_email}")

        # Act: Try to sign up again
        response = client.post(f"/activities/{activity_name}/signup?email={sample_email}")

        # Assert: Should return 400 with error
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_signup_nonexistent_activity_fails(self, client, sample_email):
        # Arrange: Use invalid activity name
        activity_name = "Nonexistent Activity"

        # Act: Make POST request to signup
        response = client.post(f"/activities/{activity_name}/signup?email={sample_email}")

        # Assert: Should return 404 with error
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]


class TestUnregisterFromActivity:
    def test_unregister_success(self, client, sample_email):
        # Arrange: First sign up
        activity_name = "Gym Class"
        client.post(f"/activities/{activity_name}/signup?email={sample_email}")

        # Act: Make DELETE request to unregister
        response = client.delete(f"/activities/{activity_name}/participants/{sample_email}")

        # Assert: Should return 200 and success message
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]

        # Assert: Participant should be removed from activity
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert sample_email not in activities[activity_name]["participants"]

    def test_unregister_nonexistent_activity_fails(self, client, sample_email):
        # Arrange: Use invalid activity name
        activity_name = "Nonexistent Activity"

        # Act: Make DELETE request to unregister
        response = client.delete(f"/activities/{activity_name}/participants/{sample_email}")

        # Assert: Should return 404 with error
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_participant_not_found(self, client):
        # Arrange: Use valid activity but email not signed up
        activity_name = "Basketball Team"
        email = "notsignedup@test.edu"

        # Act: Make DELETE request to unregister
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert: Should return 404 with error
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Participant not found" in data["detail"]