import pytest

from litestar.testing import TestClient

from kdp.apps.litestar.api.app import app



@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


def api_smoke_test(test_client: TestClient):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}


def api_map_get_test(test_client: TestClient):
    response = test_client.get("/maps/123")
    assert response.status_code == 200
    assert response.json() == {
        "dimensions": {"rows": 20, "columns": 35},
        "objects": [25]
    }


def api_map_post_test(test_client: TestClient):
    response = test_client.post("/maps", json={"rows": 20, "cols": 30})
    assert response.status_code == 201
    assert response.json() == {
        "dimensions": {"rows": 20, "columns": 30},
        "objects": []
    }
