
from tests.integration.utils.routes import client # pylint: disable=import-error

def test_get_all_search_terms():
    response = client.get("/api/searchterms/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_and_get_search_term():
    term_data = {
        "term_text": "integration-test-term"
    }
    create_resp = client.post("/api/searchterms/", json=term_data)
    assert create_resp.status_code == 201
    term = create_resp.json()
    assert term["Term"] == term_data["term_text"]

    term_id = term.get("Id") or term.get("term_id")
    get_resp = client.get(f"/api/searchterms/{term_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["Term"] == term_data["term_text"]

    # Clean up
    del_resp = client.delete(f"/api/searchterms/{term_id}")
    assert del_resp.status_code == 204

def test_delete_search_term_not_found():
    response = client.delete("/api/searchterms/99999999")
    assert response.status_code == 404

def test_get_search_term_not_found():
    response = client.get("/api/searchterms/99999999")
    assert response.status_code == 404