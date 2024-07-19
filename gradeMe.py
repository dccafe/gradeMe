import os
import sqlite3

from flask import Flask, Response, redirect, render_template, request, session, g
from flask_session import Session

from werkzeug.utils    import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from datetime  import datetime
from threading import Thread, Lock
from dbUtils   import db, init_db, saveGrade
from mspUtils  import compile, flash, runTests
from helpers   import apology, login_required, allowed_file

active_period = ''
with open('period.txt') as f:
    active_period = f.read()

# Configure application
app = Flask(__name__)
init_db(app)

# Configure Upload folder
app.config['UPLOAD_FOLDER'    ] = 'upload\\src'
app.config['SESSION_TYPE'     ] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

mspLock = Lock()

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=['GET','POST'])
@login_required
def index():

    if session['role'] == 'prof':
        # Show all students
        cursor   = db.cursor()
        students = cursor.execute("""
            SELECT   u.id, e.mod, e.num, e.grade
            FROM     user AS u 
            JOIN     exercise AS e
            ON       u.id = e.user_id
            WHERE    e.period = ? 
            AND      u.role = 'student'
            ORDER BY u.id, e.mod, e.num""",
            [active_period]).fetchall()

        grades = {}

        # s[0]: u.id, 
        for s in students:
            grades[s[0]] = {} 
            grades[s[0]][1] = {} 
            grades[s[0]][2] = {} 
            grades[s[0]][3] = {} 

        # s[1]: e.mod, s[2]: e.num, s[3]: e.grade, s[4]: e.details
        for s in students:
            grades[ s[0] ][ s[1] ][ s[2] ] = s[3]

        # Download file as a CSV
        if request.method == 'POST':
            header = ['ID']
            for module in range(1,4):            
                for exercise in range(1,21):
                    header.append(str(module) + '.' + str(exercise))

            csv = ','.join(header) + '\n'
            for student in grades:
                line = []
                line.append(str(student))
                for module in range(1,4):
                    for exercise in range(1,21):
                        if exercise in grades[student][module]:
                            line.append(str(grades[student][module][exercise]))
                        else:
                            line.append('-')
                csv += ','.join(line) + '\n'

            response = Response(csv, content_type="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=grades.csv"

            return response

        # Reply to GET request
        return render_template("allGrades.html", 
            grades=grades)


    # Show student grades
    cursor = db.cursor()
    rows = cursor.execute("""
        SELECT  mod, num, grade, details
        FROM    exercise 
        WHERE   user_id = ?
        AND     period = ?""",
        [session["user_id"], active_period]).fetchall()

    return render_template("myGrades.html", checks=rows)


@app.route("/check", methods=["GET", "POST"])
@login_required
def check():

    # If request is GET, render submission form
    if request.method == "GET":
        return render_template('check.html')

    # Request is a POST (get the file)
    if 'file' not in request.files:
        return apology('No file part')
    
    file = request.files['file']

    if file.filename == '':
        return apology('No file provided')

    filename = secure_filename(file.filename)

    if not allowed_file(filename):
        return apology('Wrong file name or extension')

    mod      = int(filename[1])
    num      = int(filename[4:6])
    newName  = session['user_id'] + '-' + filename
    fullName = os.path.join(app.config['UPLOAD_FOLDER'], newName)
    file.save(fullName)

    saveGrade(app, session['user_id'], mod, num, -1, active_period)

    def useMSP(uid, mod, num):

        mspLock.acquire()
        compile(newName)
        gdbmi = flash()
        grade, details = runTests(gdbmi, mod, num)
        saveGrade(app, uid, mod, num, grade, active_period, details)
        mspLock.release()

    Thread(target=useMSP, args=(session['user_id'], mod, num)).start()

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # Render login form
    if request.method == "GET":
        return render_template("login.html")

    # User submitted data 
    user_id  = request.form['user_id']
    password = request.form['password']

    # Ensure username was submitted
    if not user_id:
        return apology("must provide user id", 403)

    # Ensure password was submitted
    elif not password:
        return apology("must provide password", 403)

    # Query database for username
    cursor = db.cursor()
    user_data = cursor.execute("""
        SELECT hash, role 
        FROM user 
        WHERE id = ?
        """, [user_id]).fetchone()
    
    # Ensure username exists
    if user_data is None:
        return apology("Invalid user id", 403)

    pwd_hash = user_data[0]
    role     = user_data[1]

    # Ensure password is correct
    if not check_password_hash(pwd_hash, password):
        return apology("Invalid password", 403)

    # Remember which user has logged in
    session["user_id"] = user_id
    session["role"]    = role

    # Redirect user to home page
    return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == 'GET':
        return render_template('register.html')

    #Require that a user input a username,
    # implemented as a text field whose name is username.
    user_id = request.form['user_id']
    if not user_id:
        return apology("Insert your ID")

    cursor = db.cursor()
    user_in_database = cursor.execute("""
        SELECT id 
        FROM user 
        WHERE id = ?
        """, [user_id]).fetchone()

    # Check if user already exists in database
    if user_in_database:
        return apology("There is already an user with that user id")

    # Password is spelled correctly?
    password     = request.form.get('password')
    confirmation = request.form.get('confirmation')

    if not password:
        return apology("Please insert a password")

    if not confirmation:
        return apology("Please repeat the password in the confirmation box")

    # Render an apology if the passwords do not match.
    if password != confirmation:
        return apology("password and confirmation should match")

    pwd_hash = generate_password_hash(password)

    # Insert user into database
    cursor.execute("""
        INSERT INTO user (id, hash, role) 
        VALUES (?, ?, ?)""", 
        [user_id, pwd_hash, 'student'])
    
    db.commit()
    return redirect("/")

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    cursor = db.cursor()
    available_periods = cursor.execute("""
        SELECT DISTINCT period 
        FROM exercise 
        ORDER BY period
        """).fetchall()

    print(available_periods)
    #available_periods = ['2024/1', '2024/2']

    return render_template("manage.html", 
        periods=available_periods)

@app.route('/setPeriod', methods=['POST'])
def setPeriod():
    global active_period
    active_period = request.form['period']
    with open('period.txt' , 'w+') as f:
        f.write(active_period)
    return redirect("/")
