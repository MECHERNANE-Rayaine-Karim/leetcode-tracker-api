import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
from app.models.password_reset_token import PasswordResetToken
from sqlalchemy import select
import hashlib


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

def test_register_duplicate_registration(client):
    response = client.post("/users/register",
                    json={
                        "username": "user",
                        "email": "user@gmail.com",
                        "password": "password"
                    }
    )
    assert response.status_code == 200
    response = client.post("/users/register",
                json={
                    "username": "user",
                    "email": "user@gmail.com",
                    "password": "password"
                }
    )
    assert response.status_code == 409


def test_reset_fails_with_superseded_token(client):
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

    with patch("app.routers.user.resend.Emails.send") as mock_send:
        client.post("/users/forgot_password", json={"email": "user@gmail.com"})



    response = client.post("/users/reset_password",
                           json={
                               "raw_token": raw_token,
                               "new_password": "new_password"
                           }
                           )
    assert response.status_code == 401

def test_reset_fails_with_used_token(client):
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
    response = client.post("/users/reset_password",
                           json={
                               "raw_token": raw_token,
                               "new_password": "password"
                           }
                           )
    assert response.status_code == 401


def test_reset_password_fails_with_expired_token(client, db_session):
    client.post("/users/register",
        json={"username": "user", "email": "user@gmail.com", "password": "password"}
    )

    with patch("app.routers.user.resend.Emails.send") as mock_send:
        client.post("/users/forgot_password", json={"email": "user@gmail.com"})

    sent_payload = mock_send.call_args[0][0]
    raw_token = sent_payload["html"].split("token=")[1].split("'")[0]
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
    token_row = db_session.execute(
        select(PasswordResetToken).where(PasswordResetToken.hashed_token == hashed_token)
    ).scalar_one()
    token_row.expires_at = datetime.now() - timedelta(minutes=1)
    db_session.commit()

    response = client.post("/users/reset_password",
        json={"raw_token": raw_token, "new_password": "new_password"}
    )
    assert response.status_code == 401

def test_forget_password_using_nonexisting_email(client, db_session):
    client.post("/users/register",
                json={"username": "user", "email": "user@gmail.com", "password": "password"}
    )
    with patch("app.routers.user.resend.Emails.send") as mock_send:
        response = client.post("/users/forgot_password", json={"email": "email@gmail.com"})
    assert response.status_code == 200
    assert response.json() == "token has been sent"
    mock_send.assert_not_called()
    tokens = db_session.execute(select(PasswordResetToken)).scalars().all()
    assert len(tokens) == 0

