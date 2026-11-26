from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import CheckConstraint, UniqueConstraint, Index
from database.db import db

class TimestampMixin:
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)

class User(TimestampMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    last_login_at = db.Column(db.DateTime(timezone=True))
    __table_args__ = (CheckConstraint("role IN ('ADMIN','TEACHER','STUDENT')", name="ck_users_role"),)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Branch(TimestampMixin, db.Model):
    __tablename__ = "branches"
    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

class Semester(TimestampMixin, db.Model):
    __tablename__ = "semesters"
    id = db.Column(db.BigInteger, primary_key=True)
    number = db.Column(db.SmallInteger, nullable=False, unique=True)
    name = db.Column(db.String(40), nullable=False)
    __table_args__ = (CheckConstraint("number BETWEEN 1 AND 8", name="ck_semesters_number"),)

class Section(TimestampMixin, db.Model):
    __tablename__ = "sections"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    branch_id = db.Column(db.BigInteger, db.ForeignKey("branches.id", ondelete="RESTRICT"), nullable=False)
    semester_id = db.Column(db.BigInteger, db.ForeignKey("semesters.id", ondelete="RESTRICT"), nullable=False)
    academic_session = db.Column(db.String(20), nullable=False)
    __table_args__ = (UniqueConstraint("name", "branch_id", "semester_id", "academic_session",
                                       name="uq_section_cohort"),)

class Student(TimestampMixin, db.Model):
    __tablename__ = "students"
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id", ondelete="RESTRICT"),
                        unique=True, nullable=True)
    student_uid = db.Column(db.String(40), nullable=False, unique=True)
    roll_number = db.Column(db.String(30), nullable=False)
    enrollment_number = db.Column(db.String(50), nullable=False, unique=True)
    full_name = db.Column(db.String(160), nullable=False)
    photo_path = db.Column(db.String(500))
    branch_id = db.Column(db.BigInteger, db.ForeignKey("branches.id", ondelete="RESTRICT"), nullable=False)
    semester_id = db.Column(db.BigInteger, db.ForeignKey("semesters.id", ondelete="RESTRICT"), nullable=False)
    section_id = db.Column(db.BigInteger, db.ForeignKey("sections.id", ondelete="RESTRICT"), nullable=False)
    college_name = db.Column(db.String(200), nullable=False,
                             default="Bansal Group of Institutions, Bhopal")
    email = db.Column(db.String(255))
    contact_number = db.Column(db.String(20))
    academic_session = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    __table_args__ = (
        UniqueConstraint("roll_number", "branch_id", "semester_id", "section_id",
                         "academic_session", name="uq_student_roll_cohort"),
        Index("ix_students_name", "full_name"),
    )

class Teacher(TimestampMixin, db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id", ondelete="RESTRICT"),
                        unique=True, nullable=True)
    employee_code = db.Column(db.String(40), nullable=False, unique=True)
    full_name = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(255), unique=True)
    contact_number = db.Column(db.String(20))
    department = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, nullable=False, default=True)

class Subject(TimestampMixin, db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(30), nullable=False, unique=True)
    name = db.Column(db.String(160), nullable=False)
    branch_id = db.Column(db.BigInteger, db.ForeignKey("branches.id", ondelete="RESTRICT"), nullable=False)
    semester_id = db.Column(db.BigInteger, db.ForeignKey("semesters.id", ondelete="RESTRICT"), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

class TeacherSubject(TimestampMixin, db.Model):
    __tablename__ = "teacher_subjects"
    id = db.Column(db.BigInteger, primary_key=True)
    teacher_id = db.Column(db.BigInteger, db.ForeignKey("teachers.id", ondelete="RESTRICT"), nullable=False)
    subject_id = db.Column(db.BigInteger, db.ForeignKey("subjects.id", ondelete="RESTRICT"), nullable=False)
    section_id = db.Column(db.BigInteger, db.ForeignKey("sections.id", ondelete="RESTRICT"), nullable=False)
    academic_session = db.Column(db.String(20), nullable=False)
    __table_args__ = (UniqueConstraint("teacher_id", "subject_id", "section_id", "academic_session",
                                       name="uq_teacher_subject_section"),)

class AttendanceSession(TimestampMixin, db.Model):
    __tablename__ = "attendance_sessions"
    id = db.Column(db.BigInteger, primary_key=True)
    subject_id = db.Column(db.BigInteger, db.ForeignKey("subjects.id", ondelete="RESTRICT"), nullable=False)
    section_id = db.Column(db.BigInteger, db.ForeignKey("sections.id", ondelete="RESTRICT"), nullable=False)
    teacher_id = db.Column(db.BigInteger, db.ForeignKey("teachers.id", ondelete="RESTRICT"), nullable=False)
    session_date = db.Column(db.Date, nullable=False, default=date.today)
    lecture_number = db.Column(db.SmallInteger, nullable=False)
    academic_session = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="DRAFT")
    submitted_at = db.Column(db.DateTime(timezone=True))
    __table_args__ = (
        CheckConstraint("lecture_number > 0", name="ck_attendance_lecture_positive"),
        CheckConstraint("status IN ('DRAFT','SUBMITTED','LOCKED')", name="ck_attendance_session_status"),
        UniqueConstraint("subject_id", "section_id", "session_date", "lecture_number",
                         "academic_session", name="uq_attendance_lecture"),
    )

class AttendanceRecord(TimestampMixin, db.Model):
    __tablename__ = "attendance_records"
    id = db.Column(db.BigInteger, primary_key=True)
    session_id = db.Column(db.BigInteger, db.ForeignKey("attendance_sessions.id", ondelete="RESTRICT"), nullable=False)
    student_id = db.Column(db.BigInteger, db.ForeignKey("students.id", ondelete="RESTRICT"), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    marking_method = db.Column(db.String(10), nullable=False)
    marked_by_user_id = db.Column(db.BigInteger, db.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    marked_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    recognized_text = db.Column(db.String(120))
    __table_args__ = (
        CheckConstraint("status IN ('PRESENT','ABSENT','LATE','EXCUSED')", name="ck_attendance_record_status"),
        CheckConstraint("marking_method IN ('VOICE','MANUAL','IMPORT')", name="ck_attendance_method"),
        UniqueConstraint("session_id", "student_id", name="uq_attendance_student_session"),
    )

class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.BigInteger, primary_key=True)
    actor_user_id = db.Column(db.BigInteger, db.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    entity_type = db.Column(db.String(60), nullable=False)
    entity_id = db.Column(db.BigInteger, nullable=False)
    action = db.Column(db.String(60), nullable=False)
    old_values = db.Column(db.JSON)
    new_values = db.Column(db.JSON)
    reason = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
