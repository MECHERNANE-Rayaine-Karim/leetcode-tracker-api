from urllib import response

import pytest

from app.models import Problem



def test_problems_list(client,authenticated_client):
    request = client.get(
        "/problems/",
        params={"limit": 5, "offset": 0},
        headers= authenticated_client
    )
    assert request.status_code == 200
    assert request.json() == []
    request = client.post(
        "/problems/",
        json={
            "title": "Two Sum",
            "url": "https://leetcode.com/problems/two-sum/",
            "difficulty": "easy",
        },
        headers=authenticated_client
    )
    assert request.status_code == 200
    request = client.get(
        "/problems/",
        params={"limit": 5, "offset": 0},
        headers=authenticated_client
    )
    assert request.status_code == 200
    data = request.json()
    assert len(data) == 1
    assert data[0]["title"] == "Two Sum"
    assert data[0]["url"] == "https://leetcode.com/problems/two-sum/"
    assert data[0]["difficulty"] == "easy"
    assert data[0]["topics"] == []


def test_create_problem(client,authenticated_client):
    request = client.post(
        "/problems/",
        json={
            "title": "Two Sum",
            "url": "https://leetcode.com/problems/two-sum/",
            "difficulty": "easy",
        },
        headers=authenticated_client
    )
    assert request.status_code == 200
    data = request.json()
    assert data["title"] == "Two Sum"
    assert data["url"] == "https://leetcode.com/problems/two-sum/"
    assert data["difficulty"] == "easy"





def test_link_topic_problem(client,authenticated_admin):
    request = client.post(
        "/problems/",
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
        "/topics/",
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
            "topic_id" : topic_id
        },
        headers=authenticated_admin
    )
    assert request.status_code == 200
    data = request.json()["message"]
    assert data == "Topic linked to problem successfully"