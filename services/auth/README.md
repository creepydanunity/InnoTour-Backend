## 1. Clone & bootstrap

```bash
git clone git@github.com:creepydanunity/InnoTour-Backend.git
cd excursions-backend-mono

cd services/auth

touch .env
# Then open .env and fill in:
# DATABASE_URL=postgresql+asyncpg://auth_user:secret@localhost:5432/auth_db
# SECRET_KEY=<random string>

poetry install
```

---

## 2. Run migrations

```bash
# in services/auth/
alembic upgrade head
```

---

## 3. Launch the Auth Service Locally via Uvicorn

```bash
# in services/auth/
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

* **Swagger UI**: [http://localhost:8001/docs](http://localhost:8001/docs)
* **OpenAPI JSON**: [http://localhost:8001/openapi.json](http://localhost:8001/openapi.json)