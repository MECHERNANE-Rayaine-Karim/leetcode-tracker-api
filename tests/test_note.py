import pytest



def test_add_note(client,authenticated_client):
    request = client.post(
        "/problems",
        json={
            "title": "Two Sum",
            "url": "https://leetcode.com/problems/two-sum/",
            "difficulty": "easy",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    problem_id = request.json()["id"]
    request = client.post(
        f"/problems/{problem_id}/attempts",
        json={
            "used_language": "Python",
            "code_source": "just an example ......",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "status": "solved",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    attempt_id = request.json()["id"]
    request = client.post(
        f"/problems/{problem_id}/attempts/{attempt_id}/notes",
        json={
            "content": "This is a note",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    assert request.json()["content"] == "This is a note"




def test_notes_list(client,authenticated_client):
    request = client.post(
        "/problems",
        json={
            "title": "Two Sum",
            "url": "https://leetcode.com/problems/two-sum/",
            "difficulty": "easy",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    problem_id = request.json()["id"]
    request = client.post(
        f"/problems/{problem_id}/attempts",
        json={
            "used_language": "Python",
            "code_source": "just an example ......",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "status": "solved",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    attempt_id = request.json()["id"]
    request = client.post(
        f"/problems/{problem_id}/attempts/{attempt_id}/notes",
        json={
            "content": "This is a note",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    assert request.json()["content"] == "This is a note"
    note_id = request.json()["id"]
    request = client.get(
        f"/problems/{problem_id}/attempts/{attempt_id}/notes",
        headers=authenticated_client,
    )
    assert request.status_code == 200
    data = request.json()
    assert len(data) == 1
    assert data[0]["id"] == note_id

def test_edit_note(client,authenticated_client):
    request = client.post(
        "/problems",
        json={
            "title": "Two Sum",
            "url": "https://leetcode.com/problems/two-sum/",
            "difficulty": "easy",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    problem_id = request.json()["id"]
    request = client.post(
        f"/problems/{problem_id}/attempts",
        json={
            "used_language": "Python",
            "code_source": "just an example ......",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "status": "solved",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    attempt_id = request.json()["id"]
    request = client.post(
        f"/problems/{problem_id}/attempts/{attempt_id}/notes",
        json={
            "content": "This is a note",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    assert request.json()["content"] == "This is a note"
    note_id = request.json()["id"]
    request = client.patch(
        f"/problems/{problem_id}/attempts/{attempt_id}/notes/{note_id}",
        json={
            "content": "This is the edited note",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    assert request.json()["content"] == "This is the edited note"

def test_delete_note(client,authenticated_client):
    request = client.post(
        "/problems",
        json={
            "title": "Two Sum",
            "url": "https://leetcode.com/problems/two-sum/",
            "difficulty": "easy",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    problem_id = request.json()["id"]
    request = client.post(
        f"/problems/{problem_id}/attempts",
        json={
            "used_language": "Python",
            "code_source": "just an example ......",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "status": "solved",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    attempt_id = request.json()["id"]
    request = client.post(
        f"/problems/{problem_id}/attempts/{attempt_id}/notes",
        json={
            "content": "This is a note",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    assert request.json()["content"] == "This is a note"
    note_id = request.json()["id"]
    request = client.delete(
        f"/problems/{problem_id}/attempts/{attempt_id}/notes/{note_id}",
        headers=authenticated_client,
    )
    assert request.status_code == 204

def test_delete_note_rejects_other_users_note(client, authenticated_client):
    request = client.post(
        "/problems",
        json={
            "title": "Two Sum",
            "url": "https://leetcode.com/problems/two-sum/",
            "difficulty": "easy",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    problem_id = request.json()["id"]
    request = client.post(
        f"/problems/{problem_id}/attempts",
        json={
            "used_language": "Python",
            "code_source": "just an example ......",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "status": "solved",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    attempt_id = request.json()["id"]
    request = client.post(
        f"/problems/{problem_id}/attempts/{attempt_id}/notes",
        json={
            "content": "This is a note",
        },
        headers=authenticated_client,
    )
    assert request.status_code == 200
    note_id = request.json()["id"]
    client.post("/users/register", json={"username": "other", "email": "other@gmail.com", "password": "password"})
    other_login = client.post("/users/login", json={"username": "other", "password": "password"})
    other_headers = {"Authorization": f"Bearer {other_login.json()}"}
    request = client.delete(
        f"/problems/{problem_id}/attempts/{attempt_id}/notes/{note_id}",
        headers=other_headers,
    )
    assert request.status_code == 404
    request = client.get(
        f"/problems/{problem_id}/attempts/{attempt_id}/notes",
        headers=authenticated_client,
    )
    assert request.status_code == 200
    data = request.json()
    assert len(data) == 1
