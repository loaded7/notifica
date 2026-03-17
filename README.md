# Notifica API

API REST de notificações multi-canal com processamento assíncrono via filas.

![CI](https://github.com/loaded7/notifica/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)

## Demo

API em produção: https://notifica-api.onrender.com/docs

## Sobre o projeto

O Notifica é uma API que permite enviar notificações por múltiplos canais (e-mail, SMS, webhook) de forma assíncrona. O cliente envia uma requisição e recebe resposta imediata — o envio acontece em background via workers Celery, com retry automático em caso de falha.



## Funcionalidades

- Autenticação JWT (registro e login)
- Envio de notificações por e-mail, SMS e webhook
- Processamento assíncrono com Celery + Redis
- Retry automático com backoff
- Histórico de notificações por usuário
- Documentação interativa via Swagger UI
- Testes automatizados com pytest
- CI/CD com GitHub Actions

## Stack

| Tecnologia | Uso |
|---|---|
| Python 3.11 | Linguagem |
| FastAPI | Framework web |
| PostgreSQL | Banco de dados |
| SQLAlchemy | ORM |
| Celery | Processamento assíncrono |
| Redis | Message broker |
| JWT | Autenticação |
| pytest | Testes |
| GitHub Actions | CI/CD |

## Arquitetura
```
Cliente → API FastAPI → PostgreSQL
                ↓
            Redis (fila)
                ↓
        Celery Worker
                ↓
    E-mail / SMS / Webhook
```

## Como rodar localmente

### Pré-requisitos
- Python 3.11+
- Conta no [Neon](https://neon.tech) (PostgreSQL gratuito)

### Passo a passo
```bash
git clone https://github.com/loaded7/notifica.git
cd notifica

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
```

### Variáveis de ambiente
```env
DATABASE_URL=postgresql://usuario:senha@host/notifica
SECRET_KEY=sua-chave-secreta
REDIS_URL=redis://localhost:6379/0
```

### Rodando a API
```bash
uvicorn app.main:app --reload
```

Acesse: `http://localhost:8000/docs`

### Rodando os testes
```bash
pytest tests/ -v
```

## Endpoints

### Autenticação

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/v1/auth/register` | Cadastro de usuário |
| POST | `/api/v1/auth/login` | Login e geração de token |

### Notificações

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/v1/notifications/` | Criar e enfileirar notificação |
| GET | `/api/v1/notifications/` | Listar notificações do usuário |

### Exemplo de uso
```bash
# Registrar
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Thomas", "email": "thomas@email.com", "password": "123456"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "thomas@email.com", "password": "123456"}'

# Enviar notificação
curl -X POST http://localhost:8000/api/v1/notifications/ \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "email", "recipient": "dest@email.com", "subject": "Teste", "body": "Olá!"}'
```

## Testes
```
8 passed in 3s

tests/test_auth.py::test_register_success PASSED
tests/test_auth.py::test_register_duplicate_email PASSED
tests/test_auth.py::test_login_success PASSED
tests/test_auth.py::test_login_wrong_password PASSED
tests/test_notifications.py::test_create_notification_success PASSED
tests/test_notifications.py::test_create_notification_unauthenticated PASSED
tests/test_notifications.py::test_list_notifications PASSED
tests/test_notifications.py::test_notifications_isolated_by_user PASSED
```

## Autor

Thomas Modesto — [@loaded7](https://github.com/loaded7)