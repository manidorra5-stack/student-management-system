from unittest.mock import patch
from app import create_app


def test_health_endpoint_healthy():
    """Verify GET /health returns 200 and healthy payload when DB is connected."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["APP_VERSION"] = "1.0.0-test"

    with patch("app.check_db_health", return_value=(True, "connected")):
        client = app.test_client()
        response = client.get("/health")
        data = response.get_json()

        assert response.status_code == 200
        assert data["status"] == "healthy"
        assert data["service"] == "student-management-system"
        assert data["version"] == "1.0.0-test"
        assert data["database"] == "connected"


def test_health_endpoint_unhealthy():
    """Verify GET /health returns 503 when database connection fails."""
    app = create_app()
    app.config["TESTING"] = True

    with patch("app.check_db_health", return_value=(False, "Connection refused")):
        client = app.test_client()
        response = client.get("/health")
        data = response.get_json()

        assert response.status_code == 503
        assert data["status"] == "unhealthy"


def test_login_page_renders():
    """Verify login page loads properly with HTTP 200."""
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"ISGS" in response.data