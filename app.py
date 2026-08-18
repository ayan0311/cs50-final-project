from flask import Flask, render_template, session, request, redirect
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

from helpers import login_required



app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
@login_required
def index():
    return render_template ("index.html", title="Dash", super_admin=False)


# Registration and Login/Logout Routes

@app.route("/register", methods=["GET", "POST"])
def register():

    #Registering a new User
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")

        #Check for errors
        if username == "" or password == "" or confirmpassword == "":
            return render_template("register.html", title="Error", 
                                   current_route="register", 
                                   method=request.method,
                                   register_error = True,
                                   error_message = "Username/Password missing!")
        if password != confirmpassword:
            return render_template("register.html", title="Error",
                                   current_route = "register",
                                   method = request.method,
                                   register_error = True,
                                   error_message = "Password & Confirm Password didn't match!")
        
        useremail = request.form.get("email")
        userfirstname = request.form.get("firstname")
        userlastname = request.form.get("lastname")

        #insert into database (try)
        db = get_db_connection()
        try:
            db.execute(
                 "INSERT INTO users (first_name, last_name, email, username, password_hash) VALUES (?,?,?,?,?)",
                 (userfirstname, userlastname, useremail, username, generate_password_hash(password)))
        except sqlite3.IntegrityError:
            db.close()
            return render_template("register.html", title="Error",
                                               current_route = "register",
                                               method = request.method,
                                               register_error = True,
                                               error_message = "Username already Exists!")
        else:
            db.commit()
            db.close()
            return render_template("register.html", title="Registration Successful",
                                   method=request.method,
                                   current_route="register")
    else:
        return render_template ("register.html", title="Register", current_route="register", method=request.method)



@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()
    #Login a user
    if request.method == "POST":
        #Confirming if username/password was entered
        if not request.form.get("username") or not request.form.get("password"):
            return render_template("login.html", title="Login", login_error=True, current_route="login", error_message="Please enter Username/password")

        db = get_db_connection()
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        #check if username exists
        if not user:
            return render_template ("login.html", title="Error", login_error=True, current_route="login", error_message="Invalid username!")
        
        #Check if user is active
        if user["is_active"] == 0:
            return render_template ("login.html", title="Error", login_error=True, 
                                    error_message="Your account is still not active. " \
                                    "Please contact admin at ayansarkar.js@gmail.com to activate your account")
        
        #Check if password entered in correct
        if not check_password_hash(user["password_hash"], password):
            return render_template ("login.html", title="Error", login_error=True, current_route="login", error_message="Invalid password!")
        
        #remeber User who logged in:
        session["user_id"] = user["id"]

        return redirect("/")
        
    else:
        return render_template ("login.html", title="Login", current_route="login")

@app.route("/logout")
def logout():
    session.clear() # Clears Session
    return redirect("/") # Redirects to index

# End of Registration and Login/logout routes

if __name__ == "__main__":
    print("Running app...")    
    app.run(debug=True, port=5001)
    
