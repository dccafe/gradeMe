from sqlite3 import connect as dbConnect
from werkzeug.local import LocalProxy
from flask import g

def init_db(app):
    with app.app_context():
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    if 'db' not in g:
        g.db = dbConnect('gradeMe.db')
    return g.db

db = LocalProxy(get_db)

def saveGrade(app, uid, mod, num, grade, period, details=''):
    with app.app_context():

        cursor = db.cursor()

        old_grade = cursor.execute("""
            SELECT grade
            FROM   exercise
            WHERE  user_id = ? 
            AND    period = ?
            AND    mod = ?
            AND    num = ?""",
            [uid, period, mod, num]).fetchone()

        if old_grade is not None:
            cursor.execute("""
                DELETE FROM exercise 
                WHERE user_id = ?
                AND   period = ?
                AND   mod = ?
                AND   num = ? """, 
                [uid, period, mod, num])

        cursor.execute("""
            INSERT INTO exercise 
            (user_id, mod, num, grade, period, details) 
            VALUES (?, ?, ?, ?, ?, ?)""", 
            [uid, mod, num, grade, period, details])

        db.commit()

