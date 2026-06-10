from flask import Flask, render_template,request,redirect,url_for,flash
from database import get_db

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

@app.route("/records")
def records():
    conn=get_db()
    students=conn.execute('SELECT * FROM students ORDER BY NAME DESC').fetchall()
    conn.close
    return render_template("records.html",students=students)

@app.route("/notices")
def notices():
    return render_template("notice.html",notices=notice_board)


@app.route("/add_students", methods=["GET", "POST"])
def add_student():
    if request.method == 'POST':
        
        name = request.form.get('name')
        course = request.form.get('course')
        attendance = request.form.get('attendance')
        marks = request.form.get('marks')
        
        # Validation - empty check
        if not name or not course or not attendance or not marks:
            flash('❌ All fields are required!', 'danger')
            return redirect(url_for('add_student'))
        
        conn=get_db()
        conn.execute('''INSERT INTO students (name,course,attendance,marks) VALUES (?, ?, ?, ?)''',
                     (name,course,attendance,marks)
                     )
        conn.commit()
        conn.close()
                     

        
        # Data save 
        student= {
            'name':name,
            'course':course,
            'attendance': attendance,
            'marks': marks
        }
        students.append(student)
        
        # Flash message + redirect
        flash('✅ Student added successfully!', 'success')
        return redirect(url_for('records'))
    
    return render_template('add_students.html')

if __name__ == '__main__':
    app.run(debug=True)
