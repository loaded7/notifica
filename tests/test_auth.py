def test_register_success(client):
    response = client.post("/api/v1/auth/register", json={
        "name": "Thomas",
        "email": "thomas@test.com",
        "password": "123456"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "thomas@test.com"
    assert "password" not in data  # senha nunca deve vazar

def test_register_duplicate_email(client):
    client.post("/api/v1/auth/register", json={
        "name": "Thomas",
        "email": "thomas@test.com",
        "password": "123456"
    })
    response = client.post("/api/v1/auth/register", json={
        "name": "Thomas",
        "email": "thomas@test.com",
        "password": "123456"
    })
    assert response.status_code == 400
    assert "E-mail já cadastrado" in response.json()["detail"]

def test_login_success(client):
    client.post("/api/v1/auth/register", json={
        "name": "Thomas",
        "email": "thomas@test.com",
        "password": "123456"
    })
    response = client.post("/api/v1/auth/login", json={
        "email": "thomas@test.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client):
    client.post("/api/v1/auth/register", json={
        "name": "Thomas",
        "email": "thomas@test.com",
        "password": "123456"
    })
    response = client.post("/api/v1/auth/login", json={
        "email": "thomas@test.com",
        "password": "senha_errada"
    })
    assert response.status_code == 401