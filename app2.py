from flask import Flask, render_template,request,redirect,url_for,flash
from database import get_db,init_db

app = Flask(__name__)

app.secret_key = 'akshara_123'  

students=[
    {"name": "Samiksha patil",  
     "course": "Computer Engineering",
     "attendance": 85,
     "marks": 90
    },

    {"name": "Anjali shinde",
     "course": "Mechanical Engineering", 
    "attendance": 90, 
    "marks": 85
    },

    {"name": "Shivani kadam",
    "course": "Electronics and Telecommunication Engineering", 
    "attendance": 75,
    "marks": 70
    },
    {"name": "Sakshi kadam",
    "course": "Computer Engineering", 
    "attendance": 80,
    "marks": 85
    },
    {"name": "Sanika gudup",
    "course": "Mechanical Engineering", 
    "attendance": 70, 
    "marks": 75
    }
     
]

notice_board= {
    "Notice1": "Python internship started from 28 may 2026",
    "Notice2": "Python internship will be organized by Linkkiwi pvt ltd ",
    "Notice3": "Python internship  daily 2 hours from 10 am to 12 pm. "
    }

@app.route("/")
def home():
    college = {
        "college_name": "Government Polytechnic Hingoli",
        "city": "Hingoli",
        "state": "Maharashtra"
    }
    return render_template("home.html",college=college)

@app.route('/delete/<int:id>')
def delete_student(id):
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
    students=conn.execute('SELECT*FROM students WHERE id=?',(id,)).fetchone()
    conn.close()
    if students is None:
        flash("Student not found ","danger")
        return redirect(url_for("students"))
    return render_template("detail.html",students=students)



@app.route("/records")
def records():
    conn=get_db()
    students=conn.execute('SELECT * FROM students ORDER BY NAME DESC').fetchall()
    conn.close()
    return render_template("records.html",students=students)

@app.route("/notices")
def notices():
    return render_template("notice.html",notices=notice_board)


@app.route("/add_students", methods=["GET", "POST"])
def add_student():
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
                     

        
        # Data save 
        """student= {
            'name':name,
            'course':course,
            'attendance': attendance,
            'marks': marks
        }
        students.append(student)"""
        
        # Flash message + redirect
        flash('✅ Student added successfully!', 'success')
        return redirect(url_for('records'))
    
    return render_template('add_students.html')

#edit -update 
@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit_student(id):
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
    search = request.args.get('search', '')

    conn= get_db()
    students=conn.execute(""" SELECT * FROM students
                          WHERE name LIKE ?
                          OR course LIKE?
                          OR subject LIKE ?""",(f'%{search}%',f'%{search}%',f'%{search}%',)).fetchall()
    return render_template("records.html",students=students)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
