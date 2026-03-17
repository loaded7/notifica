def test_create_notification_success(authenticated_client):
    response = authenticated_client.post("/api/v1/notifications/", json={
        "channel": "email",
        "recipient": "dest@test.com",
        "subject": "Teste",
        "body": "Corpo do e-mail"
    })
    assert response.status_code == 202
    data = response.json()
    assert data["channel"] == "email"
    assert data["recipient"] == "dest@test.com"
    assert data["status"] in ["pending", "sent"]  # aceita ambos
    assert "id" in data

def test_create_notification_unauthenticated(client):
    response = client.post("/api/v1/notifications/", json={
        "channel": "email",
        "recipient": "dest@test.com",
        "subject": "Teste",
        "body": "Corpo"
    })
    assert response.status_code == 401  # sem token = bloqueado

def test_list_notifications(authenticated_client):
    authenticated_client.post("/api/v1/notifications/", json={
        "channel": "sms",
        "recipient": "+5511999999999",
        "body": "Mensagem SMS"
    })
    response = authenticated_client.get("/api/v1/notifications/")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_notifications_isolated_by_user(client):
    # Usuário 1
    client.post("/api/v1/auth/register", json={
        "name": "User1", "email": "u1@test.com", "password": "123456"
    })
    r1 = client.post("/api/v1/auth/login", json={
        "email": "u1@test.com", "password": "123456"
    })
    client.headers.update({"Authorization": f"Bearer {r1.json()['access_token']}"})
    client.post("/api/v1/notifications/", json={
        "channel": "email", "recipient": "x@x.com", "body": "msg"
    })

    # Usuário 2 não deve ver notificações do usuário 1
    client.post("/api/v1/auth/register", json={
        "name": "User2", "email": "u2@test.com", "password": "123456"
    })
    r2 = client.post("/api/v1/auth/login", json={
        "email": "u2@test.com", "password": "123456"
    })
    client.headers.update({"Authorization": f"Bearer {r2.json()['access_token']}"})
    response = client.get("/api/v1/notifications/")
    assert response.status_code == 200
    assert len(response.json()) == 0