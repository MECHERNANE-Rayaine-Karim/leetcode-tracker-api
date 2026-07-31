import pytest



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
    



