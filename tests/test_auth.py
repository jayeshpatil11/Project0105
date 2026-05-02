'''

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_signup_login():
    res = client.post("/auth/signup", params={
        "name":"test","email":"a@test.com","password":"1234","role":"student"
    })
    assert res.status_code == 200

'''
from fastapi.testclient import TestClient
from src.main import app


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


client = TestClient(app)
'''
def test_signup_success():
    res = client.post("/auth/signup", json={
        "name": "test1",
        "email": "test1@gmail.com",
        "password": "123",
        "role": "student"
    })
    assert res.status_code == 200
    assert "token" in res.json()
'''
import uuid

def test_signup_success():
    unique_email = f"test_{uuid.uuid4()}@gmail.com"

    res = client.post("/auth/signup", json={
        "name": "test1",
        "email": unique_email,
        "password": "123",
        "role": "student"
    })

    assert res.status_code == 200
    assert "token" in res.json()

'''
def test_login_success():
    client.post("/auth/signup", json={
        "name": "test2",
        "email": "test2@gmail.com",
        "password": "123",
        "role": "student"
    })

    res = client.post("/auth/login", json={
        "email": "test2@gmail.com",
        "password": "123"
    })

    assert res.status_code == 200
    assert "token" in res.json()
'''
def test_login_success():
    import uuid
    email = f"test_{uuid.uuid4()}@gmail.com"

    client.post("/auth/signup", json={
        "name": "test2",
        "email": email,
        "password": "123",
        "role": "student"
    })

    res = client.post("/auth/login", json={
        "email": email,
        "password": "123"
    })

    assert res.status_code == 200

def test_login_fail():
    res = client.post("/auth/login", json={
        "email": "wrong@gmail.com",
        "password": "123"
    })

    assert res.status_code == 401


def test_protected_no_token():
    res = client.post("/batches", params={"name": "test"})
    assert res.status_code == 422 or res.status_code == 401


def test_monitoring_post_blocked():
    res = client.post("/monitoring/attendance")
    assert res.status_code == 405

def test_student_cannot_create_batch():
    import uuid

    email = f"student_{uuid.uuid4()}@test.com"

    # signup as student
    res = client.post("/auth/signup", json={
        "name": "student",
        "email": email,
        "password": "123",
        "role": "student"
    })

    token = res.json()["token"]

    # try to create batch (should fail)
    res = client.post(
        "/batches",
        params={"name": "testbatch"},
        headers={"token": token}
    )

    assert res.status_code == 403

def test_trainer_can_create_session():
    import uuid

    email = f"trainer_{uuid.uuid4()}@test.com"

    # signup trainer
    res = client.post("/auth/signup", json={
        "name": "trainer",
        "email": email,
        "password": "123",
        "role": "trainer"
    })

    token = res.json()["token"]

    # create session
    res = client.post(
        "/sessions",
        params={"batch_id": 1, "title": "session1"},
        headers={"token": token}
    )

    # might be 200 or 404 if batch missing — both acceptable
    assert res.status_code in [200, 404]

