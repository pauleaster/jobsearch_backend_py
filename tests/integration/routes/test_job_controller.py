import pytest
from tests.integration.utils.routes import client

def test_get_all_jobs():
    response = client.get("/api/jobs/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_jobs_count():
    response = client.get("/api/jobs/count")
    assert response.status_code == 200
    assert "count" in response.json()

def test_create_and_get_job(next_job_number):
    job_data = {
        "job_number": next_job_number,
        "job_url": f"https://example.com/job/{next_job_number}",
        "title": "Integration Test Job",
        "comments": "Test comments",
        "requirements": "Test requirements"
    }
    create_resp = client.post("/api/jobs/", json=job_data)
    assert create_resp.status_code == 201
    job = create_resp.json()
    assert job["Title"] == job_data["title"]

    job_id = job.get("Id") or job.get("job_id")
    get_resp = client.get(f"/api/jobs/{job_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["Title"] == job_data["title"]

    del_resp = client.delete(f"/api/jobs/{job_id}")
    assert del_resp.status_code == 204

def test_update_job(next_job_number):
    job_data = {
        "job_number": next_job_number,
        "job_url": f"https://example.com/job/{next_job_number}",
        "title": "Job to Update",
        "comments": "Initial",
        "requirements": "Initial"
    }
    create_resp = client.post("/api/jobs/", json=job_data)
    job = create_resp.json()
    job_id = job.get("Id") or job.get("job_id")

    updated_data = job.copy()
    print("job copy JSON:", updated_data)
    updated_data["Title"] = "Updated Title"
    print("updated_data JSON:", updated_data)
    put_resp = client.put(f"/api/jobs/{job_id}", json=updated_data)
    assert put_resp.status_code == 200

    # Debug print
    print("PUT response JSON:", put_resp.json())

    # Use the alias "Title" as returned by the API
    assert put_resp.json()["Title"] == "Updated Title"

    client.delete(f"/api/jobs/{job_id}")

def test_patch_job_field(next_job_number):
    job_data = {
        "job_number": next_job_number,
        "job_url": f"https://example.com/job/{next_job_number}",
        "title": "Patch Test",
        "comments": "Patch me",
        "requirements": "Patch me"
    }
    create_resp = client.post("/api/jobs/", json=job_data)
    job = create_resp.json()
    job_id = job.get("Id") or job.get("job_id")

    patch_data = {"field": "comments", "value": "Patched!"}
    patch_resp = client.patch(f"/api/jobs/{job_id}", json=patch_data)
    assert patch_resp.status_code == 200
    assert patch_resp.json()["comments"] == "Patched!"

    client.delete(f"/api/jobs/{job_id}")