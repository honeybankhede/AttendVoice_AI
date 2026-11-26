# Database Design

## Tables
1. `users`: authentication identity, role, active state.
2. `branches`: academic branch catalogue.
3. `semesters`: semesters 1–8.
4. `sections`: section + branch + semester + academic session.
5. `students`: identity, roll/enrollment number, photo path and cohort.
6. `teachers`: employee profile.
7. `subjects`: branch- and semester-specific subject catalogue.
8. `teacher_subjects`: teacher-to-subject-to-section assignment.
9. `attendance_sessions`: one lecture attendance event.
10. `attendance_records`: one student's attendance result for a lecture.
11. `audit_logs`: append-oriented record of administrative changes.

## Attendance percentage
For a student and subject:
`(count of PRESENT records / count of conducted attendance sessions) * 100`

The final calculation must define how LATE and EXCUSED are treated according to
college policy. The initial default should count PRESENT as present and all
submitted sessions as conducted. Draft sessions must not affect percentages.

## Retention
Ordinary teacher actions must not hard-delete attendance. Use correction actions
with an audit entry. Database backups and restore procedures must be configured
before production deployment.
