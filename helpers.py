from flask import redirect, session
from functools import wraps
import sqlite3

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_current_user():
    db = get_db_connection()

    user = db.execute("SELECT is_admin FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    return user
