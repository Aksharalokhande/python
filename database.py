import sqlite3
from flask import Flask,render_template,redirect,request,url_for,flash
app=Flask(__name__)
app.secret_key="akshara123"

def get_db():
   """database connection"""
   conn=sqlite3.connect('college.db')
   conn.row_factory= sqlite3.Row
   return conn

def init_db():
    """Create Table"""
    conn=get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS students(
                
                 name TEXT NOT NULL,
                 course TEXT NOT NULL,
                 attendance INTEGER DEFAULT 0,
                 marks INTEGER NOT NULL)
                 '''
    )
    conn.commit()
    conn.close()
if __name__ == "__main__":
    init_db()
    app.run(debug=True)