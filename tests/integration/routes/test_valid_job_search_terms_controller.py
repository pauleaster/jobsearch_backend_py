
from tests.integration.utils.routes import client  # pylint: disable=import-error

def test_get_valid_job_search_terms():
    response = client.get("/api/validJobsAndSearchTerms")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Check structure of at least one item if present
    if data:
        item = data[0]
        assert "job_id" in item
        assert "job_number" in item
        assert "matching_terms" in item

def test_post_filtered_valid_job_search_terms():
    # Example filter payload
    payload = {
        "filterTerms": ["python", "remote"],
        "currentJob": True,
        "appliedJob": False
    }
    response = client.post("/api/filteredJobsAndSearchTerms", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Check structure of at least one item if present
    if data:
        item = data[0]
        assert "job_id" in item
        assert "job_number" in item
        assert "matching_terms" in item