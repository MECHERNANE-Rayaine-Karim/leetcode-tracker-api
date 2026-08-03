import pytest



def test_add_topic(client,authenticated_admin):
    request = client.post(
        "/topics",
        json={
            "name": "Arrays",
        },
        headers=authenticated_admin
    )
    assert request.status_code == 200
    assert request.json()["name"] == "Arrays"




def test_get_problems_by_topic(client,authenticated_admin):
    request = client.post(
        "/problems",
        json={
            "title": "Two Sum",
            "url": "https://leetcode.com/problems/two-sum/",
            "difficulty": "easy",
        },
        headers=authenticated_admin
    )
    assert request.status_code == 200
    problem_id = request.json()["id"]
    request = client.post(
        "/topics",
        json={
            "name": "Arrays",
        },
        headers=authenticated_admin
    )
    assert request.status_code == 200
    topic_id = request.json()["id"]
    request = client.post(
        f"/problems/{problem_id}/topics",
        params={
            "topic_id": topic_id
        },
        headers=authenticated_admin
    )
    assert request.status_code == 200
    assert request.json()["message"] == "Topic linked to problem successfully"
    request = client.get(
        f"topics/{topic_id}/problems",
        headers=authenticated_admin
    )
    assert request.status_code == 200
    data = request.json()
    assert len(data) == 1
    assert data[0]["id"] == problem_id


def test_edit_topic(client,authenticated_admin):
    request = client.post(
        "/topics",
        json={
            "name": "Arrays",
        },
        headers=authenticated_admin
    )
    assert request.status_code == 200
    assert request.json()["name"] == "Arrays"
    topic_id = request.json()["id"]
    request = client.patch(
        f"topics/{topic_id}",
        json={
            "name": "linked lists",
        },
        headers=authenticated_admin
    )
    assert request.status_code == 200
    assert request.json()["name"] == "linked lists"





def test_delete_topic_not_linked(client,authenticated_admin):
    request = client.post(
        "/topics",
        json={
            "name": "Arrays",
        },
        headers=authenticated_admin
    )
    assert request.status_code == 200
    assert request.json()["name"] == "Arrays"
    topic_id = request.json()["id"]
    request = client.delete(
        f"topics/{topic_id}",
        headers=authenticated_admin
    )
    assert request.status_code == 204

def test_delete_topic_linked_to_problems(client,authenticated_admin):
    request = client.post(
        "/problems",
        json={
            "title": "Two Sum",
            "url": "https://leetcode.com/problems/two-sum/",
            "difficulty": "easy",
        },
        headers=authenticated_admin
    )
    assert request.status_code == 200
    problem_id = request.json()["id"]
    request = client.post(
        "/topics",
        json={
            "name": "Arrays",
        },
        headers=authenticated_admin
    )
    assert request.status_code == 200
    topic_id = request.json()["id"]
    request = client.post(
        f"/problems/{problem_id}/topics",
        params={
            "topic_id": topic_id
        },
        headers=authenticated_admin
    )
    assert request.status_code == 200
    assert request.json()["message"] == "Topic linked to problem successfully"
    request = client.delete(
        f"topics/{topic_id}",
        headers=authenticated_admin
    )
    assert request.status_code == 204