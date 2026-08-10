from flask import Flask, render_template, session
from flask_session import Session
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db():
    return mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
    )

@app.route("/")
def index():
    session.clear()
    #session["user_id"] = "ayan"
    return render_template ("login.html", title="Login", super_admin=False)


# Registration and Login/Logout Routes

@app.route("/register")
def register():
    return render_template ("register.html", title="Register", current_route="register")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template ("login.html", title="Login", current_route="login", login_error=True, 
                            error_message="Your username is still not approved, contact superadmin at ayansarkar.js@gmail.com")

@app.route("/logout")
def logout():
    session.clear() # Clears Session
    return redirect("/") # Redirects to index

# End of Registration and Login/logout routes

if __name__ == "__main__":
    print("Running app...")    
    app.run(debug=True)
    
