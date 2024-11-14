from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
app = Flask(__name__)

# Kết nối tới cơ sở dữ liệu
conn = psycopg2.connect(
    host="localhost",
    database="web_management",
    user="postgres", 
    password="1"
)
cursor = conn.cursor()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Nhận thông tin chỉnh sửa từ form
        student_id = request.form['student_id']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        major = request.form['major']
          
        # Cập nhật thông tin sinh viên trong cơ sở dữ liệu
        cursor.execute("UPDATE students SET name = %s, age = %s, gender = %s, major = %s WHERE id = %s", 
                       (name, age, gender, major, student_id))
        conn.commit()
        return redirect('/')

    
    # Lấy danh sách sinh viên để hiển thị
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('index.html', students=students)


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_id = request.form['id']  
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        major = request.form['major']
        cursor.execute("INSERT INTO students (id, name, age, gender, major) VALUES (%s, %s, %s, %s, %s)", 
                       (student_id, name, age, gender, major))
        conn.commit()
        return redirect('/')
    return render_template('add_student.html')  # Hiển thị trang thêm sinh viên


@app.route('/delete', methods=['POST'])
def delete_student():
    student_id = request.form['student_id']
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)