import sqlite3

class UsernameExistsError(Exception):
    pass

class EntryError(Exception):
    pass

def update_login_log(db, user_id, activity):
    try:
        db.execute(
            "INSERT INTO login_logs (user_id, activity) VALUES (?,?)",
            (user_id, activity)
         )
    except sqlite3.IntegrityError or sqlite3.OperationalError or sqlite3.ProgrammingError:
        raise EntryError
    else:
        db.commit()

def get_current_user(db, user_id):
    user = db.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,)).fetchone()
    return user

def get_user(db, username):
    user = db.execute("SELECT * FROM users WHERE username = ?", (username, )).fetchone()
    return user

def create_user(db, fn, ln, email, username, password):
    try:
        db.execute(
                "INSERT INTO users (first_name, last_name, email, username, password_hash) VALUES (?,?,?,?,?)",
                (fn, ln, email, username, password))
    except sqlite3.IntegrityError:
        raise UsernameExistsError
    else:
        db.commit()