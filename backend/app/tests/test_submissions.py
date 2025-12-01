import pytest


@pytest.mark.asyncio
class TestSubmitEndpoint:
    async def test_submit_success(self, client):
        """Test of successful data sending"""
        submission_data = {
            "date": "2024-01-15",
            "first_name": "John",
            "last_name": "Doe",
        }

        async for client_instance in client:
            response = await client_instance.post("/api/submit", json=submission_data)
            assert response.status_code == 200
            assert response.json()["success"]

    async def test_submit_whitespace_validation(self, client):
        """Test of presence spaces in names"""
        submission_data = {
            "date": "2024-01-15",
            "first_name": "John Smith",
            "last_name": "Doe",
        }

        async for client_instance in client:
            response = await client_instance.post("/api/submit", json=submission_data)
            assert response.status_code == 400
            data = response.json()
            assert "error" in data
            assert "first_name" in data["error"]

    async def test_submit_empty_fields(self, client):
        """Test ob blank fields"""
        submission_data = {"date": "2024-01-15", "first_name": "", "last_name": "Doe"}

        async for client_instance in client:
            response = await client_instance.post("/api/submit", json=submission_data)
            assert response.status_code == 400
            data = response.json()
            assert "error" in data


@pytest.mark.asyncio
class TestHistoryEndpoint:
    async def test_history_success(self, client):
        """Test of getting history"""
        async for client_instance in client:
            # Creating test data
            submissions = [
                {"date": "2024-01-15", "first_name": "John", "last_name": "Doe"},
                {"date": "2024-01-16", "first_name": "John", "last_name": "Doe"},
            ]

            for submission in submissions:
                response = await client_instance.post("/api/submit", json=submission)
                assert response.status_code == 200

            # Testing of history
            response = await client_instance.get(
                "/api/history", params={"date": "2024-01-16"}
            )
            assert response.status_code == 200
            data = response.json()
            assert "items" in data
            assert "total" in data
            # Check if our records present, precise count isn't necessary
            assert data["total"] >= 2
            john_records = [
                item for item in data["items"] if item["first_name"] == "John"
            ]
            assert len(john_records) >= 2

    async def test_history_with_filters(self, client):
        """Test of history with filters"""
        async for client_instance in client:
            # Creating test data
            submissions = [
                {"date": "2024-01-15", "first_name": "John", "last_name": "Doe"},
                {"date": "2024-01-15", "first_name": "Jane", "last_name": "Doe"},
            ]

            for submission in submissions:
                response = await client_instance.post("/api/submit", json=submission)
                assert response.status_code == 200

            # Test with filter by name
            response = await client_instance.get(
                "/api/history", params={"date": "2024-01-15", "first_name": "John"}
            )
            assert response.status_code == 200
            data = response.json()
            # Check if all records are filtered correctly
            if data["items"]:
                assert all(item["first_name"] == "John" for item in data["items"])

    async def test_history_no_data(self, client):
        """Test of history with no data"""
        async for client_instance in client:
            response = await client_instance.get(
                "/api/history", params={"date": "1900-01-01"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 0
            assert data["items"] == []
