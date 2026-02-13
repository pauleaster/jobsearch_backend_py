import pytest
from tests.integration.utils.routes import client

@pytest.fixture
def next_job_number():
    resp = client.get("/api/jobs/")
    assert resp.status_code == 200
    jobs = resp.json()

    nums = [j.get("job_number") for j in jobs if j.get("job_number") is not None]
    return (max(nums) if nums else 0) + 1