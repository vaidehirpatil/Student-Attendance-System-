from flask import Flask, render_template, request, redirect, url_for, session # type: ignore
from database import init_db, get_db # type: ignore
from models import authenticate_user, get_students, mark_attendance, get_attendance # type: ignore

app = Flask(__name__)
app.secret_key = "secret_key"

init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        return "Invalid Credentials!"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark():
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    students = get_students(db)
    
    if request.method == 'POST':
        for student_id in students:
            status = request.form.get(f'student_{student_id}', 'absent')
            mark_attendance(db, student_id, status)
        return redirect(url_for('dashboard'))

    return render_template('mark_attendance.html', students=students)

@app.route('/view_attendance')
def view_attendance():
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    attendance_records = get_attendance(db)
    return render_template('view_attendance.html', records=attendance_records)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
