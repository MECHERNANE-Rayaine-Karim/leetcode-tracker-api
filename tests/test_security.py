import pytest
from app.services.security import hash_password, verify_password


def test_hash_password_creates_different_hash_than_plaintext():
    plain_password = "Rayaine"
    hashed_password = hash_password(plain_password)
    assert hashed_password != plain_password

def test_verify_password_works_with_correct_password():
    plain_password = "Rayaine"
    hashed_password = hash_password(plain_password)
    assert verify_password(plain_password,hashed_password) is True

def test_verify_password_fails_with_wrong_password():
    hashed_password = hash_password("Rayain")
    assert verify_password("Rayaine",hashed_password) is False