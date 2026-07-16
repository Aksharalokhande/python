from http import client
from click import prompt
from flask import Flask, render_template,request,redirect,url_for,flash,session
from flask.cli import load_dotenv
from database import get_db,init_db
from groq import Groq
import os
from werkzeug.security import generate_password_hash,check_password_hash
import os
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

app = Flask(__name__)


app.secret_key = 'akshara_123'  

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route("/")
def home():
    

    conn = get_db()
    

    total_students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    avg_marks = conn.execute(
        "SELECT AVG(marks) FROM students"
    ).fetchone()[0]

    avg_attendance = conn.execute(
        "SELECT AVG(attendance) FROM students"
    ).fetchone()[0]

    top_students = conn.execute(
        "SELECT * FROM students ORDER BY marks DESC LIMIT 5"
    ).fetchall()


    

    return render_template(
        'home.html',
        total_students=total_students,
        avg_marks=round(avg_marks or 0, 2),
        avg_attendance=round(avg_attendance or 0, 2),
        top_students=top_students, )


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')
    
    


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username  = request.form['username'].strip()
        password = request.form['password']

        conn = get_db()
        existing = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if existing:
            flash('username already exist!', 'danger')
            conn.close()
            return render_template('register.html')
        hashed = generate_password_hash(password)
        conn.execute('INSERT INTO users(username,password,role) VALUES (?,?,?)',(username,hashed,'student'))
        conn.commit() 
        conn.close() 
        
        flash('Register successfully! please login', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username  = request.form['username'].strip()
        password = request.form['password']

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        print("username",username)
        print("user",user)


        if user and check_password_hash(user['password'],password):
            session['username'] = username
            session['role'] = user['role']
            flash(f'welcome {username}!','success')
            return redirect(url_for('home'))
        else:

            flash('Invalid username or password', 'danger')
            
    return render_template('login.html')
        

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))






@app.route('/delete/<int:id>')
def delete_student(id):
    if session.get('role') !='admin':
        flash("Admins only! You do not have permission","danger")
        return redirect(url_for('home'))
    
    conn=get_db()

    #first checke if it exists
    students=conn.execute('SELECT * FROM students WHERE id=?',(id,)).fetchone()
    if students is None:
        flash("Student not found","danger")
        conn.close()
        return redirect(url_for('students'))
    conn.execute('DELETE FROM students WHERE id =?',(id,))
    conn.commit()
    conn.close()
    flash("Student deleted successfully","success")
    return redirect(url_for('records'))





@app.route('/students/<int:id>')
def student_detail(id):
    conn=get_db()
    student = conn.execute('SELECT*FROM students WHERE id=?',(id,)).fetchone()
    conn.close()
    if student is None:
        flash("Student not found ","danger")
        return redirect(url_for("records"))
    return render_template("detail.html",student=student)



@app.route("/records")
def records():
    conn=get_db()
    students=conn.execute('SELECT * FROM students ORDER BY NAME DESC').fetchall()
    conn.close()
    return render_template("records.html",students=students)


@app.route("/students/<int:id>/tip")
def get_ai_tip(id):
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    if student is None:
        os.abort(404)  # trigger 404.html
    prompt = f"""
    Student name: {student['name']}
    Subject: {student['subject']}
    Marks: {student['marks']}/100
    Attendance: {student['attendance']}%
    Please provide practical study tips, In simple and encouraging tone. It should not be more than 2 lines.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    tip = response.choices[0].message.content
    return render_template("detail.html", student=student, tip=tip)


@app.route("/add_students", methods=["GET", "POST"])
def add_student():
    if session.get('role') !='admin':
        flash("Admins only! You do not have permission","danger")
        return redirect(url_for('home'))

    
    if request.method == 'POST':
        
        name = request.form.get('name')
        roll = request.form.get('roll')
        course = request.form.get('course')
        subject= request.form.get('subject')
        marks = request.form.get('marks')
        attendance = request.form.get('attendance')
        
        
        # Validation - empty check
        if not name or not roll or not course or not  subject or not attendance or not marks:
            flash('❌ All fields are required!', 'danger')
            return redirect(url_for('add_student'))
        
        conn=get_db()
        conn.execute('''INSERT INTO students (name,roll,course,subject,attendance,marks) VALUES (?, ?, ?, ?, ?, ?)''',
                     (name,roll,course,subject,attendance,marks)
                     )
        conn.commit()
        conn.close()
       # print(f"Received new student: {name}")
                     

        
        
        
        # Flash message + redirect
        flash('✅ Student added successfully!', 'success')
        return redirect(url_for('records'))
    
    return render_template('add_students.html')

#edit -update 
@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit_student(id):

    if session.get('role') !='admin':
        flash("Admins only! You do not have permission","danger")
        return redirect(url_for('home'))
    
    conn=get_db()
   
    if request.method=='POST':

        name=request.form['name']
        roll=request.form['roll']
        course=request.form['course']
        subject=request.form['subject']
        marks=request.form['marks']
        attendance=request.form['attendance']
        
        if not id:
            flash("id cannot be empty","danger")
            return redirect(url_for("edit_student",id=id))
        conn.execute("""UPDATE students
                    SET name=? ,roll=? ,course=?, subject=?, marks=? ,attendance=?
                    WHERE id=? """,(name , roll, course, subject, marks, attendance,id)
                    )
        conn.commit()
        conn.close()
        flash(f"{name} Updated successfully!","success")
        return redirect(url_for('records')) 
    
    students=conn.execute(
       "SELECT * FROM students WHERE id=?",
       (id,))
    student=students.fetchone()
    conn.close()
    return render_template('edit_student.html',student=student)

@app.route('/search')
def search_student():
    q = request.args.get('q', '')

    conn= get_db()
    if q:

        students = conn.execute(""" SELECT * FROM students
                        WHERE name LIKE ?
                        OR course LIKE?
                        OR subject LIKE ?
                        OR roll LIKE ?""",(f'%{q}%',f'%{q}%',f'%{q}%',f'%{q}%')).fetchall()
    else:
        students = conn.execute('SELECT * FROM students ORDER BY id DESC').fetchall()  
    conn.close()
    return render_template("records.html",students=students,query=q)


@app.route('/filter')
def filter_students():
    subject = request.args.get('subject','')
    selected_result = request.args.get('result','')
    conn = get_db()
    subjects = conn.execute('''SELECT DISTINCT subject FROM students
                        WHERE subject IS NOT NULL
                        AND subject !=""
                        ORDER BY subject ASC ''').fetchall()
    
    query = 'SELECT * FROM students WHERE 1=1'
    params = []

    if subject:
        query += ' AND subject = ?'
        params.append(subject)

    if selected_result == 'pass':
        query += ' AND marks >= 40'

    elif selected_result == 'fail':
        query += ' AND marks < 40'

    query += ' ORDER BY id DESC'   

    students = conn.execute(query,params).fetchall()
    conn.close()

    return render_template('filter.html',students=students,selected_subject=subject, subjects=subjects,selected_result=selected_result)



#  Notice Page
@app.route("/notices")
def notices():
    conn = get_db()
    notices = conn.execute(
        "SELECT * FROM notices ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template(
        "notices.html",
        notices=notices
    )




# Add Notice
@app.route("/add_notice", methods=["POST"])
def add_notice():
    notice = request.form["notice"]
    date = request.form["date"]

    conn = get_db()
    conn.execute(
        "INSERT INTO notices(notice,date) VALUES(?,?)",
        (notice,date)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("notices"))


# Delete Notice
@app.route("/delete_notice/<int:id>")
def delete_notice(id):
    if session.get('role') !='admin':
        flash("Admins only! You do not have permission","danger")
        return redirect(url_for('home'))

    conn = get_db()
    conn.execute(
        "DELETE FROM notices WHERE id=?",
        (id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("notices"))


# Edit Notice
@app.route("/edit_notice/<int:id>", methods=["GET", "POST"])
def edit_notice(id):
    if session.get('role') !='admin':
        flash("Admins only! You do not have permission","danger")
        return redirect(url_for('home'))

    conn = get_db()

    if request.method == "POST":

        notice = request.form["notice"]
        date = request.form["date"]

        conn.execute(
            "UPDATE notices SET notice=?, date=? WHERE id=?",
            (notice,date, id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("notices"))

    notice = conn.execute(
        "SELECT * FROM notices WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_notice.html",
        notice=notice
    )

@app.route('/faculty')
def faculty():
    conn = get_db()
    faculty = conn.execute("SELECT * FROM faculty").fetchall()
    conn.close()
    return render_template("faculty.html", faculty=faculty)

@app.route('/faculty/add', methods=['GET', 'POST'])
def add_faculty():

    if session.get('role') !='admin':
        flash("Admins only! You do not have permission","danger")
        return redirect(url_for('home'))

    if request.method == 'POST':
        faculty_id = request.form['faculty_id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']
        subject = request.form['subject']
        designation = request.form['designation']

        conn = get_db()

        conn.execute("""
            INSERT INTO faculty
            (faculty_id, name, email, phone, course, subject, designation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (faculty_id, name, email, phone, course, subject, designation))

        conn.commit()
        conn.close()

        flash("Faculty added successfully!", "success")
        return redirect(url_for('faculty'))

    return render_template("add_faculty.html")


@app.route('/faculty/view/<faculty_id>')
def view_faculty(faculty_id):
    conn = get_db()
    faculty = conn.execute("SELECT * FROM faculty WHERE faculty_id = ?",(faculty_id,)).fetchone()
   
    conn.close()
    return render_template("view_faculty.html", faculty=faculty)

@app.route('/faculty/edit/<faculty_id>', methods=['GET', 'POST'])
def edit_faculty(faculty_id):

    if session.get('role') !='admin':
        flash("Admins only! You do not have permission","danger")
        return redirect(url_for('home'))

    conn = get_db()

    if request.method == 'POST':
        conn.execute("""
            UPDATE faculty
            SET name=?, email=?, phone=?, course=?, subject=?, designation=?
            WHERE faculty_id=?
        """, (
            request.form['name'],
            request.form['email'],
            request.form['phone'],
            request.form['course'],
            request.form['subject'],
            request.form['designation'],
            faculty_id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('faculty'))

    faculty = conn.execute(
        "SELECT * FROM faculty WHERE faculty_id=?",
        (faculty_id,)
    ).fetchone()
    conn.close()

    return render_template("edit_faculty.html", faculty=faculty)

@app.route('/faculty/delete/<faculty_id>')
def delete_faculty(faculty_id):

    if session.get('role') !='admin':
        flash("Admins only! You do not have permission","danger")
        return redirect(url_for('home'))

    conn = get_db()
    conn.execute(
        "DELETE FROM faculty WHERE faculty_id=?",
        (faculty_id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('faculty'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


init_db()
if __name__ == '__main__':

    app.run(debug=True)
