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

def test_sync_topics_problem(client, authenticated_admin):
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
    arrays_id = request.json()["id"]
    link = client.post(
        f"/problems/{problem_id}/topics",
        params={"topic_id": arrays_id},
        headers=authenticated_admin
    )
    assert link.status_code == 200
    topic1 = client.post("/topics", json={"name": "Linked List"}, headers=authenticated_admin)
    topic2 = client.post("/topics", json={"name": "Hash Table"}, headers=authenticated_admin)
    assert topic1.status_code == 200
    assert topic2.status_code == 200
    topic1_id = topic1.json()["id"]
    topic2_id = topic2.json()["id"]

    request = client.put(
        f"/problems/{problem_id}/topics",
        json=[topic1_id, topic2_id],
        headers=authenticated_admin
    )
    assert request.status_code == 200
    returned_ids = {t["id"] for t in request.json()}
    assert returned_ids == {topic1_id, topic2_id}

def test_delete_topic_rejects_regular_user(client, authenticated_admin,authenticated_client):
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
        headers=authenticated_client
    )
    assert request.status_code == 403
    request = client.get("topics", headers=authenticated_client)
    assert request.status_code == 200
    assert any(t["id"] == topic_id for t in request.json())