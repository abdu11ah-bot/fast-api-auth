# Forge API

A FastAPI authentication backend built step-by-step to learn and implement secure JWT-based authentication.

## Project Goal

Forge API is a learning-focused backend project covering the complete authentication flow:

- User registration
- Password hashing with Argon2
- User login
- JWT access tokens
- JWT refresh tokens
- Protected routes
- Authentication dependencies
- Environment-based configuration
- Separation of models, schemas, security, routers, and dependencies

The project is intentionally structured like a real backend application so the concepts can later be extended into a production API.

---

## Tech Stack

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**
- **Pydantic Settings**
- **pwdlib + Argon2**
- **python-jose**
- **Uvicorn**

---

## Project Structure

```text
forge-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── connection.py
│   │   └── dependencies.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── user.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── users.py
│   │
│   └── dependencies/
│       ├── __init__.py
│       └── auth.py
│
├── forge.db
├── .env
├── .gitignore
└── requirements.txt
```

---

## Architecture

The authentication system follows this flow:

```text
database/
    ↓
models/user.py
    ↓
schemas/auth.py
    ↓
core/security.py
    ↓
routers/auth.py
    ↓
POST /auth/register
    ↓
POST /auth/login
    ↓
dependencies/auth.py
    ↓
GET /users/me
    ↓
refresh tokens
    ↓
authorization
```

---

## Authentication Flow

### 1. Registration

```text
Client
  ↓
POST /auth/register
  ↓
Validate input
  ↓
Check email
  ↓
Hash password
  ↓
Save user
  ↓
Return safe user data
```

Plain passwords are never stored in the database.

Example request:

```json
{
  "email": "test@gmail.com",
  "password": "TestPassword123"
}
```

Example response:

```json
{
  "id": 1,
  "email": "test@gmail.com"
}
```

---

### 2. Login

```text
Client
  ↓
POST /auth/login
  ↓
Find user by email
  ↓
Verify password hash
  ↓
Create access token
  ↓
Create refresh token
  ↓
Return tokens
```

Example response:

```json
{
  "access_token": "ACCESS_TOKEN",
  "refresh_token": "REFRESH_TOKEN",
  "token_type": "bearer"
}
```

---

### 3. Access Token

The access token is short-lived and is used to access protected API endpoints.

Example:

```http
Authorization: Bearer ACCESS_TOKEN
```

The JWT contains information such as:

```json
{
  "sub": "1",
  "exp": 1780000000,
  "type": "access"
}
```

- `sub` = user ID
- `exp` = expiration time
- `type` = token purpose

JWT payloads are signed, not encrypted. Sensitive information should not be placed inside them.

---

### 4. Protected Route

Example:

```http
GET /users/me
```

The request includes:

```http
Authorization: Bearer ACCESS_TOKEN
```

FastAPI uses:

```text
OAuth2PasswordBearer
        ↓
get_current_user()
        ↓
decode JWT
        ↓
validate token
        ↓
extract user ID
        ↓
find user in database
        ↓
return current user
```

---

### 5. Refresh Token

When the access token expires:

```text
Access token expired
        ↓
POST /auth/refresh
        ↓
Send refresh token
        ↓
Verify JWT
        ↓
Verify token type = refresh
        ↓
Find user
        ↓
Create new access token
```

Example request:

```json
{
  "refresh_token": "REFRESH_TOKEN"
}
```

The refresh endpoint must reject an access token used as a refresh token.

---

## API Endpoints

| Method | Endpoint | Authentication | Purpose |
|---|---|---|---|
| GET | `/` | No | API status |
| POST | `/auth/register` | No | Register a user |
| POST | `/auth/login` | No | Login and receive tokens |
| POST | `/auth/refresh` | No | Generate a new access token |
| GET | `/users/me` | Yes | Get current authenticated user |

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd forge-api
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root:

```env
JWT_SECRET_KEY=replace-this-with-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Never commit `.env` to Git.

Generate a strong secret for real deployments instead of using a simple development value.

---

## Run the API

From the project root:

```bash
python -m uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## Testing the Authentication Flow

### Step 1 — Register

```http
POST /auth/register
```

```json
{
  "email": "test@gmail.com",
  "password": "TestPassword123"
}
```

### Step 2 — Login

```http
POST /auth/login
```

```json
{
  "email": "test@gmail.com",
  "password": "TestPassword123"
}
```

Copy the returned `access_token`.

### Step 3 — Access Protected Route

```http
GET /users/me
```

Add:

```http
Authorization: Bearer <access_token>
```

Expected:

```json
{
  "id": 1,
  "email": "test@gmail.com"
}
```

### Step 4 — Refresh

When the access token expires:

```http
POST /auth/refresh
```

```json
{
  "refresh_token": "<refresh_token>"
}
```

A new access token should be returned.

---

## Security Principles

Forge API currently follows these important authentication principles:

- Passwords are never stored as plaintext.
- Passwords are hashed with Argon2.
- Password verification uses the password-hashing library.
- JWT secrets are loaded from environment variables.
- `.env` is excluded from Git.
- Access tokens are short-lived.
- Access and refresh tokens have different purposes.
- JWT algorithms are explicitly specified during verification.
- Token expiration is validated.
- Protected routes do not trust a user ID supplied by the client.
- Login failures use a generic credential error.
- Password hashes are excluded from API responses.
- Refresh tokens are checked for the correct token type.
- HTTPS should be used in production.

---

## Current Security Limitation

The current refresh-token implementation is intentionally simplified for learning.

It currently does **not** provide:

- Refresh-token rotation
- Refresh-token database storage
- Refresh-token revocation
- Logout token invalidation
- Token reuse detection
- Rate limiting
- Account lockout
- Role-based authorization
- Ownership-based authorization

These are planned extensions for the next stages of Forge API.

---

## Learning Roadmap

### Completed

- [x] Database setup
- [x] SQLAlchemy User model
- [x] Pydantic authentication schemas
- [x] Password hashing
- [x] Password verification
- [x] JWT access tokens
- [x] User registration
- [x] User login
- [x] Authentication dependency
- [x] Protected `/users/me` endpoint
- [x] Environment-based JWT configuration
- [x] Refresh tokens
- [x] `/auth/refresh`

### Next

- [ ] Refresh-token rotation
- [ ] Refresh-token revocation
- [ ] Logout
- [ ] Authorization
- [ ] User roles
- [ ] Ownership checks
- [ ] Rate limiting
- [ ] CORS
- [ ] CSRF considerations for cookie-based refresh tokens
- [ ] PostgreSQL
- [ ] Alembic migrations
- [ ] Automated tests
- [ ] Docker
- [ ] Production deployment

---

## Core Concepts Learned

This project is designed to understand the difference between:

```text
Authentication
    ↓
Who are you?

Authorization
    ↓
What are you allowed to do?
```

And:

```text
Password
    ↓
Argon2 hash
    ↓
Database
```

versus:

```text
Login
    ↓
JWT access token
    ↓
Protected API
```

and:

```text
Refresh token
    ↓
New access token
```

---

## Disclaimer

This project is primarily a learning implementation. Before using the authentication system in a production application, additional security controls, testing, monitoring, secret management, token revocation, and deployment hardening should be added.
