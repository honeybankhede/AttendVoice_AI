# AttendVoice AI — Phase 1 Quick Guide

1. Open the extracted project folder in VS Code.
2. Follow the Windows setup in the root README.
3. Start PostgreSQL.
4. Create and apply the first migration.
5. Run `python app.py`.
6. Open `/api/health` and confirm the database is connected.

The next phase will add secure login, password reset policy, role-based access
control, and the first admin account creation flow. Do not create a production
admin account by inserting a weak or hard-coded password directly into SQL.
