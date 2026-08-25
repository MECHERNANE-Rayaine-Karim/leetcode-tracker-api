import pytest
from unittest.mock import patch



def test_register_user_create_new_user(client):
    response = client.post( "/users/register",
        json={
            "username":"user",
            "email":"user@gmail.com",
            "password":"password"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "user"
    assert data["email"] == "user@gmail.com"
    assert "hashed_password" not in data

def test_login_user_returns_a_token(client):
    client.post("/users/register",
            json={
                "username": "user",
                "email": "user@gmail.com",
                "password": "password"
            }
    )
    response = client.post( "/users/login",
            json={
                "username":"user",
                "password":"password"
            }
    )
    assert response.status_code == 200
    token = response.json()
    assert isinstance(token, str)
    assert len(token.split(".")) == 3

def test_login_user_fails_when_wrong_password(client):
    client.post("/users/register",
                json={
                    "username": "user",
                    "email": "user@gmail.com",
                    "password": "password"
                }
    )
    response = client.post("/users/login",
                json={
                    "username": "user",
                    "password": "wrong_password"
                }
    )
    assert response.status_code == 401

def test_forgot_password(client):
    client.post("/users/register",
        json={
            "username": "user",
            "email": "user@gmail.com",
            "password": "password"
        }
    )
    with patch("app.routers.user.resend.Emails.send") as mock_send:
        response = client.post("/users/forgot_password",
            json={
                "email": "user@gmail.com"
            }
        )
    assert response.status_code == 200
    assert response.json() == "token has been sent"
    mock_send.assert_called_once()


def test_reset_password(client):
    client.post("/users/register",
        json={
            "username": "user",
            "email": "user@gmail.com",
            "password": "password"
        }
    )

    with patch("app.routers.user.resend.Emails.send") as mock_send:
        client.post("/users/forgot_password", json={"email": "user@gmail.com"})

    sent_payload = mock_send.call_args[0][0]
    raw_token = sent_payload["html"].split("token=")[1].split("'")[0]

    response = client.post("/users/reset_password",
        json={
            "raw_token": raw_token,
            "new_password": "new_password"
        }
    )
    assert response.status_code == 200

    login_response = client.post("/users/login",
        json={
            "username": "user",
            "password": "new_password"
        }
    )
    assert login_response.status_code == 200



