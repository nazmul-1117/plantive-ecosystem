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
│   ├── routers/          # API route definitions (HTTP endpoints)
│   ├── controllers/      # Request orchestration and response handling
│   ├── services/         # Business logic and application rules
│   ├── repositories/     # Database access layer (CRUD operations)
│   ├── models/           # SQLModel database models (tables)
│   ├── schemas/          # Pydantic request and response schemas
│   ├── dependencies/     # Reusable FastAPI dependencies
│   ├── middleware/       # Custom middleware (authentication, logging, etc.)
│   ├── exceptions/       # Custom exceptions and global exception handlers
│   ├── core/             # Core configuration (settings, database, security)
│   └── __init__.py
│
├── migrations/           # Alembic database migration files
├── .env.example          # Example environment variables
├── alembic.ini           # Alembic configuration
├── main.py               # FastAPI application entry point
├── pyproject.toml        # Project dependencies and configuration
└── README.md             # Project documentation
```

---

## 🏗️ Application Flow

```text
Client Request
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
Repository
      │
      ▼
PostgreSQL Database
```

### Layer Responsibilities

| Layer | Responsibility |
|--------|----------------|
| **Router** | Defines API endpoints and delegates requests to controllers. |
| **Controller** | Coordinates request handling and prepares responses. |
| **Service** | Contains business logic and application rules. |
| **Repository** | Handles all database operations using SQLModel. |
| **Models** | SQLModel table definitions mapped to PostgreSQL. |
| **Schemas** | Pydantic models for request validation and API responses. |
| **Dependencies** | Reusable dependency injection (e.g., database sessions, authentication). |
| **Middleware** | Processes requests/responses globally (authentication, logging, CORS, etc.). |
| **Exceptions** | Custom exceptions and centralized error handling. |
| **Core** | Application configuration, security, database, and shared utilities. |

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