# Workforce Compliance & Scheduling Assistant

A backend system for managing staff, shifts, and compliance tracking.

---

## 📂 Project Structure

root/
├─ docker-compose.yaml
├─ be/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  ├─ pyproject.toml
│  ├─ pytest.ini
│  ├─ src/
│  │  ├─ main.py
│  │  ├─ api/
│  │  ├─ core/
│  │  ├─ db/
│  │  ├─ schemas/
│  │  └─ service/
│  └─ tests/
└─ db/
   ├─ schema.sql
   └─ seed.sql

---

## ⚡ Features

- User management (staff, supervisors, managers)
- Shift scheduling with overlap validation
- Staff certifications and compliance tracking
- Notes and incidents tracking
- API endpoints via FastAPI
- PostgreSQL database backend

---

## 🛠️ Prerequisites

- Docker
- Docker Compose

---

## 🚀 Setup & Running

### 1. Build and run services

```
docker-compose up --build
```

This will:

- Start PostgreSQL (`workforce-postgres`)
- Run your backend app in a container

### 2. Access the backend

- FastAPI server: `http://localhost:8000`
- API docs (Swagger): `http://localhost:8000/docs`
- API docs (ReDoc): `http://localhost:8000/redoc`

---

## ⚡ Running Tests

From the project root:

```
docker-compose run app pytest tests -v --disable-warnings
```

- Make sure the backend is **not already running** on port 8000 (optional)
- Tests use the same Dockerized Postgres database

---

## 🐘 Database

- Schema and seed data are located in `db/schema.sql` and `db/seed.sql`
- PostgreSQL container `workforce-postgres` will automatically initialize using these files
- Database URL inside Docker:

```
postgresql+psycopg2://postgres:postgres@postgres:5432/workforce_db
```

---

## 📬 Using Postman / API Requests

1. Open Postman and create a new request
2. Set the URL:

```
http://localhost:8000/<endpoint>
```

3. Select HTTP method (GET, POST, PUT, DELETE)
4. For POST/PUT requests, set **Body → raw → JSON**. Example:

```
{
  "site_id": "11111111-aaaa-1111-aaaa-111111111112",
  "shift_date": "2025-12-24",
  "shift_type": "morning",
  "start_time": "2025-12-24T08:00:00Z",
  "end_time": "2025-12-24T16:00:00Z"
}
```

5. Add headers if needed:

```
Content-Type: application/json
Authorization: Bearer <token>
```

---

## ⚙️ Notes / Tips

- Inside Docker, **do not use `localhost`** for the database. Use `postgres` as hostname
- Use volumes for live development:

```
volumes:
  - ./be/src:/app/src
  - ./be/tests:/app/tests
```

- For code changes with hot reload, run:

```
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

---

This README provides essential instructions for developers or testers to get started quickly.