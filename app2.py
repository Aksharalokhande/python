from flask import Flask, render_template

from app1 import college
app = Flask(__name__)
students=[
    {"name": "samiksha patil",  
     "course": "Computer Engineering",
     "attendance": 85,
     "marks": 90
    },

    {"name": "anjali shinde",
     "course": "Mechanical Engineering", 
    "attendance": 90, 
    "marks": 85
    },

    {"name": "shivani kadam",
    "course": "Electronics and Telecommunication Engineering", 
    "attendance": 75,
    "marks": 70
    },
    {"name": "sakshi kadam",
    "course": "Computer Engineering", 
    "attendance": 80,
    "marks": 85
    },
    {"name": "sanika gudup",
    "course": "Mechanical Engineering", 
    "attendance": 70, 
    "marks": 75
    }
     
]

notice_board= {
    "notice1": "Python internship started from 28 may 2026",
    "notice2": "Python internship will be organized by LinKkiwi pvt ltd ",
    "notice3": "Python internship  daily 2 hours from 10 am to 12 pm. "
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
    return render_template("records.html",students=students)

@app.route("/notices")
def notices():
    return render_template("notice.html",notices=notice_board)

if __name__ =="__main__":
    app.run(debug=True)