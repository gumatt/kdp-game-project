import pytest
from litestar.testing import TestClient

from kdp.apps.litestar.api.app import app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


def api_smoke_test(test_client: TestClient):
    response = test_client.get("/")
    assert response.status_code == 200  # noqa: W291, PLR2004
    assert response.json() == {"message": "Hello World!"}


def api_map_get_test(test_client: TestClient):
    response = test_client.get("/maps/123")
    assert response.status_code == 200  # noqa: PLR2004
    assert response.json()["size"] == {"rows": 20, "columns": 35}
    assert len(response.json()["objects"]) == 1


def api_map_post_test(test_client: TestClient):
    response = test_client.post(
        "/maps",
        json={"dimensions": {"rows": 20, "columns": 30}, "objects": []},
    )
    assert response.status_code == 201  # noqa: PLR2004
    assert response.json() == {"size": {"rows": 20, "columns": 30}, "objects": []}
