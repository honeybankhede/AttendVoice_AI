# AttendVoice AI — Architecture

## Phase 1 scope
This release creates the Flask application foundation, PostgreSQL connection,
SQLAlchemy data model, database migration support, health endpoint, and project
documentation. Authentication and user-facing management workflows are later phases.

## Architecture
- Browser: HTML, CSS, JavaScript (future UI modules)
- Application: Flask application factory and REST endpoints
- Persistence: PostgreSQL 16
- ORM: Flask-SQLAlchemy / SQLAlchemy
- Schema versioning: Flask-Migrate (Alembic)

## Main relationships
- `users` contains login identities and roles.
- `students.user_id` and `teachers.user_id` optionally link a profile to a login.
- `branches`, `semesters`, and `sections` define the academic cohort.
- `subjects` belong to a branch and semester.
- `teacher_subjects` assigns a teacher to a subject and section for an academic session.
- `attendance_sessions` represents one lecture.
- `attendance_records` stores one student's status within that lecture.
- `audit_logs` records authorized changes.

## Data integrity decisions
- Roll numbers are unique within a branch/semester/section/academic-session cohort.
- Enrollment numbers, student UIDs, user emails, employee codes and subject codes are unique.
- `(session_id, student_id)` is unique, preventing duplicate marks in one lecture.
- Foreign keys use RESTRICT to protect historical attendance from accidental deletion.
- Attendance session status supports DRAFT, SUBMITTED and LOCKED.
- Attendance record status and marking method are constrained at database level.

## Important implementation note
A student roll number can be reused in another cohort or academic session, so it is
not globally unique. Voice matching must always happen inside the selected section
and academic session. Store photo paths, not public photo URLs; serve photos through
an authenticated route in the student-management phase.
