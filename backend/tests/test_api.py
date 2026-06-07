"""Integration tests for the Jumble Solver API endpoints.

The test client uses PERMISSIVE mode by default (via the solver fixture).
Mode-specific tests explicitly pass the ``mode`` field in the request body.
"""

from fastapi.testclient import TestClient


class TestSolveEndpoint:
    """POST /api/solve"""

    def test_solve_endpoint(self, client: TestClient) -> None:
        response = client.post("/api/solve", json={"letters": "dog", "mode": "permissive"})
        assert response.status_code == 200
        data = response.json()
        assert "matches" in data
        assert "execution_ms" in data
        assert "total_matches" in data
        assert "input" in data
        assert data["input"] == "dog"
        assert "mode" in data
        assert "filtered_count" in data

    def test_solve_results(self, client: TestClient) -> None:
        response = client.post("/api/solve", json={"letters": "dog", "mode": "permissive"})
        data = response.json()
        words = [m["word"] for m in data["matches"]]
        assert "dog" in words
        assert "god" in words
        assert "do" in words
        assert "go" in words
        assert data["total_matches"] == 4
        assert data["full_anagram_count"] == 2
        assert data["sub_anagram_count"] == 2

    def test_solve_uppercase(self, client: TestClient) -> None:
        response = client.post("/api/solve", json={"letters": "DOG", "mode": "permissive"})
        assert response.status_code == 200
        assert response.json()["total_matches"] == 4

    def test_solve_confidence_fields(self, client: TestClient) -> None:
        response = client.post("/api/solve", json={"letters": "dog", "mode": "permissive"})
        data = response.json()
        for match in data["matches"]:
            assert "confidence" in match
            assert "category" in match
            assert "zipf_score" in match
            assert 0.0 <= match["confidence"] <= 1.0


class TestSolveModes:
    """Test different solving modes via the API."""

    def test_strict_mode(self, client: TestClient) -> None:
        response = client.post("/api/solve", json={"letters": "dog", "mode": "strict"})
        assert response.status_code == 200
        data = response.json()
        assert data["mode"] == "strict"
        words = [m["word"] for m in data["matches"]]
        # Common words should still appear in strict mode
        assert "dog" in words
        assert "god" in words

    def test_default_mode_is_strict(self, client: TestClient) -> None:
        response = client.post("/api/solve", json={"letters": "dog"})
        assert response.status_code == 200
        data = response.json()
        assert data["mode"] == "strict"

    def test_permissive_mode(self, client: TestClient) -> None:
        response = client.post("/api/solve", json={"letters": "dog", "mode": "permissive"})
        assert response.status_code == 200
        data = response.json()
        assert data["mode"] == "permissive"
        assert data["filtered_count"] == 0


class TestHealthEndpoint:
    """GET /api/health"""

    def test_health_endpoint(self, client: TestClient) -> None:
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["dictionary_size"] == 11
        assert data["version"] == "2.0.0"


class TestStatsEndpoint:
    """GET /api/stats"""

    def test_stats_endpoint(self, client: TestClient) -> None:
        response = client.get("/api/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_words"] == 11
        assert data["min_length"] == 2
        assert data["max_length"] == 5
        assert "avg_length" in data


class TestModesEndpoint:
    """GET /api/modes"""

    def test_modes_endpoint(self, client: TestClient) -> None:
        response = client.get("/api/modes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 5
        mode_names = [m["mode"] for m in data]
        assert "strict" in mode_names
        assert "permissive" in mode_names

    def test_mode_has_description(self, client: TestClient) -> None:
        response = client.get("/api/modes")
        data = response.json()
        for mode_info in data:
            assert "description" in mode_info
            assert len(mode_info["description"]) > 10


class TestInvalidInput:
    """Validation errors should return 422."""

    def test_invalid_input(self, client: TestClient) -> None:
        response = client.post("/api/solve", json={"letters": "123"})
        assert response.status_code == 422

    def test_empty_input(self, client: TestClient) -> None:
        response = client.post("/api/solve", json={"letters": ""})
        assert response.status_code == 422

    def test_missing_field(self, client: TestClient) -> None:
        response = client.post("/api/solve", json={})
        assert response.status_code == 422

    def test_too_long_input(self, client: TestClient) -> None:
        response = client.post("/api/solve", json={"letters": "a" * 21})
        assert response.status_code == 422

    def test_invalid_mode(self, client: TestClient) -> None:
        response = client.post("/api/solve", json={"letters": "dog", "mode": "invalid"})
        assert response.status_code == 422
