
from flask import Flask
app = Flask(__name__)

college_info = {
    "college_name": "GOVERNMENT POLYTECHNIC HINGOLI",
    "City": "Hingoli",
    "State": "Maharashtra",
    "Courses": ["Computer Engineering", "Mechanical Engineering", 
                "Electronics and Telecommunication Engineering"],
    "principal": "B.P Devasarkar",}

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
#route 1 homepage
@app.route('/')
def home():
    return """
    <h1>College Smart Portal</h1>
    <p>This project manages college and student records using flask.</p>
    """
#route 2 student records
@app.route("/students")
def student_records():
    output ="<h2>Student Records</h2>"
    for student in students:
        output +=f"""
        <p>
        Name:{student['name']}<br>
        Course:{student['course']}<br>
        Marks:{student['marks']}<br>
        Attendance:{student['attendance']}%
        </p>
        <hr>
        """
        return output
@app.route("/college")
def college():
    return f"""
    <h2>College Information</h2>

<p>College Name: {college_info['college_name']}</p>
<p>City: {college_info['City']}</p>
<p>State: {college_info['State']}</p>
<p>Courses: {(college_info['Courses'])}</p>
<p>Principal: {college_info['principal']}</p>
"""


if __name__ == "__main__":
    app.run(debug=True)