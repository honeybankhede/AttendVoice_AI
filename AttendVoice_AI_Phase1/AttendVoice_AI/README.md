# AttendVoice AI
Smart Voice-Based Attendance & Student Identity Management System

College: Bansal Group of Institutions, Bhopal

## Phase 1 included
- Flask application foundation
- PostgreSQL 16 configuration
- SQLAlchemy models for core academic and attendance entities
- Flask-Migrate support
- Database health endpoint
- Architecture and database documentation
- Docker Compose PostgreSQL service

## Prerequisites
- Python 3.10 or newer
- VS Code
- Docker Desktop (recommended) OR a locally installed PostgreSQL server

## Windows setup (VS Code)

### 1. Extract and open
Extract `AttendVoice_AI.zip`. In VS Code choose **File → Open Folder** and select
the extracted `AttendVoice_AI` folder.

### 2. Create a virtual environment
Open **Terminal → New Terminal** in VS Code and run:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once in the same terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again.

### 3. Install packages

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment

Copy `.env.example` and name the copy `.env`.
You can do this in File Explorer or run:

```powershell
Copy-Item .env.example .env
```

For local development, the example secret and database password are placeholders.
Change them before deployment.

### 5. Start PostgreSQL using Docker

If Docker Desktop is installed and running:

```powershell
docker compose up -d
```

This creates the `attendvoice_db` database and starts PostgreSQL on port 5432.

If you use a local PostgreSQL installation instead, create a database named
`attendvoice_db`, a user named `attendvoice`, and update `DATABASE_URL` in `.env`
to match your local credentials.

### 6. Create database migration

```powershell
flask --app app db init
flask --app app db migrate -m "Initial AttendVoice schema"
flask --app app db upgrade
```

Run `db init` only the first time. Migration files are created in the `migrations/`
folder and should be committed to source control.

### 7. Run the application

```powershell
python app.py
```

Open these URLs:
- http://127.0.0.1:5000/
- http://127.0.0.1:5000/api/health

The health endpoint should report `"database": "connected"`.

## Common issues
- **Connection refused:** Ensure PostgreSQL/Docker is running and port 5432 is free.
- **Password authentication failed:** Check username, password and database name in `.env`.
- **`flask` not found:** Activate `.venv` and reinstall requirements.
- **PowerShell activation blocked:** Use the process-scoped execution policy command above.

## Security before production
- Replace `SECRET_KEY` with a cryptographically random secret.
- Use a strong PostgreSQL password and private database networking.
- Set `FLASK_DEBUG=false`.
- Do not commit `.env` or student photographs.
- Restrict photo access behind authenticated routes.
- Configure encrypted backups, HTTPS, logging and retention policies.
- Apply role and ownership checks in every attendance API before deployment.

## Current status
Phase 1 is the database and application foundation. It does not yet implement
login screens, admin/teacher/student workflows, voice recognition, attendance
submission or exports. These are the next development phases.
