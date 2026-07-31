# AGENTS.md

FastAPI + SQLAlchemy supplier-management app (Lagobo Distribuciones S.A.S.). Spanish UI text and code comments. No tests, linter, or CI configured — verify manually by starting the server.

## Commands
- Setup: `python -m venv venv`, `pip install -r requirements.txt`
- Run: `uvicorn main:app --host 127.0.1.1 --port 8000` (note `127.0.1.1`, per README)
- `main.py` calls `create_tables()` at import, so the SQLite DB auto-creates on startup
- Seed/user scripts (run from repo root):
  - `python crear_admin.py` — creates `admin@lagobo.com` / `Admin123!`
  - `python inicializar_datos_base.py` — seeds TypeUser 1-4
  - `python gestionar_usuarios.py listar|crear <email> <pass> <tipo>|reset <email> <pass>` — user management CLI

## Database
- Default DB is SQLite `management_providers.db` (gitignored). Real engine is `app/database/core.py`; `DATABASE_URL` env var switches to Postgres. `app/config/config.py`'s `DATABASE_URL` is a dead constant — don't rely on it.
- `.env` is NOT tracked (gitignored) and must be created from `.env.example`. It contains `SECRET_KEY` + `ALGORITHM` and (optionally) production Postgres creds, but does NOT set `DATABASE_URL`, so local runs always use SQLite.

## Auth (gotchas)
- Active login flow: `app/crud/post/post_login.py` → `app/middleware/security.py` `create_access_token` (python-jose) using `SECRET_KEY` loaded from the environment via `load_dotenv()`. `app/middleware/current_user.py` decodes with the same env key. If `SECRET_KEY` is missing, `security.py` raises at import and the server won't start — so `.env` is required.
- `app/middleware/create_token.py` (PyJWT, uses `.env` `SECRET_KEY`) is effectively unused — don't change it expecting auth behavior to change.
- Passwords are Argon2 via `app/middleware/hasher.py` (`hasher()` to hash, `verify_password()` to check). Any seeding code must use `hasher()`.

## Architecture
- `app/api/<method>/…` = FastAPI routers, `app/crud/` = DB logic, `app/schemas/` = pydantic, `app/models/` = SQLAlchemy models (submissions live in `submission_models.py` with `SubmissionStatus`/`RiskLevel` enums stored as strings).
- Routers are registered in `main.py`; several existing files are NOT mounted (e.g. `get_type_document`, `get_region`, `get_type_user`). Many endpoints are also defined inline in `main.py` (`/api/cities`, `/api/countries`, `/api/offices`, `/api/ciiu`, `/api/user/profile`) — check `main.py` before assuming an endpoint lives in `app/api/`.
- Frontend is static HTML/JS served by FastAPI: `app/pages` mounted at `/pages`, page routes return `FileResponse`. Frontend stores the JWT in `localStorage` (`token`, `type_user`, `is_admin`).
- Login response MUST include `type_user` and `is_admin` (frontend depends on it) — keep that contract when touching `post_login`.
- Uploaded documents go to `app/uploads/<submission_id>/` (gitignored).

## Conventions
- Branch per README: `feature/`, `fix/`, `refactor/` names; commits use conventional prefixes (`feat:`, `fix:`, `chore:`).
- Keep new user-facing strings and comments in Spanish.
- No real `numpy` dependency in `requirements.txt` (the old `nnumpy` typosquat was removed) — install real `numpy`/`pandas` explicitly when adding numeric deps.