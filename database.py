import os
import sqlite3
from flask import Flask,render_template,redirect,request,url_for,flash
app=Flask(__name__)
app.secret_key="akshara123"

BASE_DTR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DTR, 'college.db')


def get_db():
   """database connection"""
   conn=sqlite3.connect(DB_PATH)
   conn.row_factory= sqlite3.Row
   return conn

def init_db():
    """Create Table"""
    conn=get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS students(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 roll INTEGER NOT NULL,
                 course TEXT NOT NULL,
                 subject TEXT NOT NULL,
                 marks INTEGER NOT NULL,
                 attendance INTEGER DEFAULT 0
                 )
                 '''
    )

    conn.execute('''CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL UNIQUE,
                 password TEXT NOT NULL

                 )
                 '''
    )
    try:
        conn.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'student'")
    except Exception:
        pass

    conn.execute('''CREATE TABLE IF NOT EXISTS notices(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                notice TEXT NOT NULL,
                date TEXT NOT NULL

                 )
                 '''
    )
    conn.execute('''CREATE TABLE IF NOT EXISTS faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    course TEXT,
    subject TEXT,
    designation TEXT 
                )'''
    )


    

    conn.commit()
    conn.close()
    
init_db()
if __name__ == "__main__":
    
    app.run(debug=True)