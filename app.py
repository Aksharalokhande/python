from flask import Flask
app =Flask(__name__)
@app.route('/')
def home():
    return '<h1> College Portal</h1>'

@app.route('/about')
def about():
    return '<h1> About College Portal</h1><p>This is simple college management system.</p>'

@app.route('/students')
def students():
    return '<h1> Students List</h1><p>All students will show here.</p>'




if __name__ =='__main__':
    app.run(debug=True)
    