#college smart portal project using lists,for loop,functions and dictionaries

college_info = {
    "college_name": "GOVERNMENT POLYTECHNIC HINGOLI",
    "City": "Hingoli",
    "State": "Maharashtra",
    "Courses": ["Computer Engineering", "Mechanical Engineering", 
                "Electronics and Telecommunication Engineering"],
    "principal": "B.P Devasarkar",}

students =[
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
    "notice1": "python intership satrted from 28 may 2026",
    "notice2": "python internship wii be organized by linkiwi pvt ltd ",
    "notice3": "python internship  daily 2 hours from 10 am to 12 pm "
    }

student_login={
    "samiksha patil": "123",
    "anjali shinde": "456",
    "shivani kadam": "789",
    "sakshi kadam": "321",
    "sanika gudup": "654"
}
print("----STUDENT LOGIN----")
username=input("Enter username: ")
password=input("Enter password: ")
if username in student_login and student_login[username] == password:
    print("Login successful!")
else:
    print("Invalid username or password.")


def get_status(attendance):
    if attendance >= 75:
        return "Eligible"
    else:
        return "short attendance"
    
    #search student

def search_records(name):
    for student in students:
        if student["name"] == name:
            return student
    return "student not found"


print("----COLLEGE INFORMATION----")
print(f"College Name: {college_info['college_name']}")
print(f"City: {college_info['City']}")
print(f"State: {college_info['State']}")
print(f"Courses: {(college_info['Courses'])}")
print(f"Principal: {college_info['principal']}")


print("\n----STUDENT RECORDS----")
for student in students:

    print(f"Name: {student['name']}, Course: {student['course']},marks: {student['marks']}, Attendance: {student['attendance']}%,Login Status:{student['login_status']},eligibility: {get_status(student['attendance'])}")

print("\n----NOTICE BOARD----")
for key, value in notice_board.items():
    print(f"{key}: {value}")

print("\n----SEARCH RESULTS----") 
search_record=input("Enter student name to search: ")
result=search_records(search_record)
print(result)