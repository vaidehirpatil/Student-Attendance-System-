from database import get_db # type: ignore

def authenticate_user(username, password):
    db = get_db()
    user = db.execute("SELECT * FROM professors WHERE username = ? AND password = ?", (username, password)).fetchone()
    return user is not None

def get_students(db):
    return db.execute("SELECT id, name FROM students").fetchall()

def mark_attendance(db, student_id, status):
    db.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, DATE('now'), ?)", (student_id, status))
    db.commit()

def get_attendance(db):
    return db.execute("SELECT students.name, COUNT(CASE WHEN status = 'present' THEN 1 END) AS present_days, COUNT(CASE WHEN status = 'absent' THEN 1 END) AS absent_days FROM attendance JOIN students ON attendance.student_id = students.id GROUP BY students.id").fetchall()
