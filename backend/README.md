# 🌿 Plantive Ecosystem Backend

A modern, open-source backend for the **Plantive Ecosystem**, built with **FastAPI**, **SQLModel**, and **PostgreSQL**.

Plantive aims to be an all-in-one platform for plant lovers, gardeners, and smart garden enthusiasts by combining plant management, AI assistance, community features, and a marketplace into a single ecosystem.

> 🚧 **Project Status:** Active Development

---

# ✨ Features

* 🔐 JWT Authentication & Authorization
* 👤 User Management
* 🌱 Plant Catalog
* 🏡 Garden Management
* 🤖 AI Plant Assistant
* 💬 Community (Posts, Comments, Likes)
* 🛒 Marketplace
* 🔔 Notifications
* 📊 Alembic Database Migrations
* ⚡ Async FastAPI + SQLModel

---

# 🛠️ Tech Stack

| Category         | Technology      |
| ---------------- | --------------- |
| Language         | Python 3.13+    |
| Framework        | FastAPI         |
| ORM              | SQLModel        |
| Database         | PostgreSQL      |
| Migrations       | Alembic         |
| Validation       | Pydantic        |
| Authentication   | JWT             |
| Password Hashing | pwdlib (Argon2) |
| Package Manager  | uv              |
| ASGI Server      | Uvicorn         |

---

# 📁 Project Structure

```text
backend/
│
├── app/
│   ├── routers/          # API endpoints
│   ├── controllers/      # Request orchestration
│   ├── services/         # Business logic
│   ├── models/           # SQLModel models
│   ├── schemas/          # Request & response schemas
│   ├── middleware/       # Authentication & exception handlers
│   └── config/           # Settings, database, security
│
├── migrations/           # Database migrations
├── main.py               # Application entry point
└── pyproject.toml
```

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/nazmul-1117/plantive-ecosystem.git

cd backend
```

---

## 2. Install dependencies

Using **uv**

```bash
uv sync
```

---

## 3. Create a PostgreSQL database

Example

```text
plantive_db
```

---

## 4. Configure environment variables

Create a `.env` file.

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/plantive_db

JWT_SECRET_KEY=change-me
JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## 5. Apply database migrations

```bash
uv run alembic upgrade head
```

---

## 6. Start the development server

```bash
uv run uvicorn main:app --reload
```

---

# 📖 API Documentation

After starting the server

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# 🔐 Authentication

Plantive uses **JWT Bearer Authentication**.

Typical authentication flow

```
Register
      │
      ▼
Login
      │
      ▼
Access Token + Refresh Token
      │
      ▼
Protected API Requests
```

Every authenticated request must include

```http
Authorization: Bearer <access_token>
```

---

# 🏗️ Architecture

```
HTTP Request
      │
      ▼
 Router
      │
      ▼
 Controller
      │
      ▼
 Service
      │
      ▼
 SQLModel
      │
      ▼
 PostgreSQL
```

---

# 🗄️ Database Migrations

Create a migration

```bash
uv run alembic revision --autogenerate -m "describe changes"
```

Apply migrations

```bash
uv run alembic upgrade head
```

Rollback one migration

```bash
uv run alembic downgrade -1
```

---

# 🤝 Contributing

Contributions are welcome!

If you'd like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

Please make sure your code follows the project's coding style and includes appropriate tests where applicable.

---

# 📌 Roadmap

* [ ] Authentication
* [ ] Email Verification
* [ ] Password Reset
* [ ] Plant Catalog
* [ ] Garden Management
* [ ] Plant Care Reminders
* [ ] AI Plant Diagnosis
* [ ] Community Module
* [ ] Marketplace
* [ ] Notifications
* [ ] Admin Dashboard
* [ ] Docker Support
* [ ] CI/CD Pipeline
* [ ] Unit & Integration Tests

---

# 📄 License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

# ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub. It helps others discover the project and motivates continued development.