
 from flask import Flask, request, render_template
import sqlite3

app = Flask(_name_)

def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            conn.cursor().executescript(f.read())
        conn.commit()
        conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    course = request.form['course']
    
    conn = get_db_connection()
    conn.execute("INSERT INTO students (name, email, phone, course) VALUES (?, ?, ?, ?)", (name, email, phone, course))
    conn.commit()
    conn.close()
    
    return 'Form submitted successfully!'

@app.route('/update_form/<int:id>', methods=['POST'])
def update_form(id):
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    course = request.form['course']
    
    conn = get_db_connection()
    conn.execute("UPDATE students SET name=?, email=?, phone=?, course=? WHERE id=?", (name, email, phone, course, id))
    conn.commit()
    conn.close()
    
    return 'Form updated successfully!'

@app.route('/delete_form/<int:id>', methods=['POST'])
def delete_form(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    
    return 'Form deleted successfully!'

if _name_ == '_main_':
    app.run(debug=True)