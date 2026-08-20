from flask import Flask, render_template, session, request, redirect, g
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import dbtools
from helpers import login_required


app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Database Connections
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("database.db")
        g.db.row_factory = sqlite3.Row

    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()
#Database Connections

#Index Page
@app.route("/")
@login_required
def index():
    user = dbtools.get_current_user(get_db(), session["user_id"])
    return render_template ("index.html", title="Dash", admin=user["is_admin"])


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
        try:
            dbtools.create_user(get_db(), userfirstname, userlastname, useremail, username, generate_password_hash(password))
        except dbtools.UsernameExistsError:
            return render_template("register.html", title="Error",
                                               current_route = "register",
                                               method = request.method,
                                               register_error = True,
                                               error_message = "Username already Exists!")
        else:
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

        username = request.form.get("username")
        password = request.form.get("password")
        user = dbtools.get_user(get_db(), username)

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
        

        #update the login_log:
        try:
            dbtools.update_login_log(get_db(), user["id"], 'login')
        except dbtools.EntryError:
            return render_template ("login.html", title="Error", login_error=True, current_route="login", 
                                    error_message="Something went wrong, login again!")
        else:
            #remeber User who logged in:
            session["user_id"] = user["id"]

        return redirect("/")
        
    else:
        return render_template ("login.html", title="Login", current_route="login")

@app.route("/logout")
def logout():
    try:
        dbtools.update_login_log(get_db(), session["user_id"], 'logout')
    except dbtools.EntryError:
        return redirect("/logout")
    else:
        session.clear() # Clears Session
        return redirect("/") # Redirects to index

# End of Registration and Login/logout routes

if __name__ == "__main__":
    print("Running app...")    
    app.run(debug=True, port=5001)
    
