import os 
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

#configure application
app = Flask(__name__)
#ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOADED"] = True

#ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#configure sqlite3 db
db  = SQL("sqlite:///manager.db")

#the home page
@app.route("/")
@login_required
def index():
    apps= db.execute("SELECT * FROM apps WHERE app_id = ?", session["user_id"])
    
    return render_template("index.html",apps=apps)

# registration page
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        surname = request.form.get("surname")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        username = request.form.get("username")
        #error checking
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not username:
            return apology("Must provide username", 400)
        elif len(rows) != 0:
            return apology("Username already exist", 400)
        elif not firstname or not surname:
            return apology("Must provide your personal details", 400)
        elif not password:
            return apology("Must provide password", 400)
        elif not confirmation:
            return apology("Must provide a confirmation password", 400)
        elif not password == confirmation:
            return apology("Passwords must match", 400)
        else: 
            # generate hash of the password
            hash = generate_password_hash(password,method="pbkdf2:sha256")
            #insert new user
            db.execute("INSERT INTO users (firstname,surname, password, username) VALUES (?,?,?,?)",firstname,surname,hash,username)
            #redirect user to home page
            return redirect("/")
    return render_template("register.html")

#Login page
@app.route("/login", methods=["GET","POST"])
def login():
    #forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("You must provide your username", 403)
        elif not request.form.get("password"):
            return apology("You must provide a password", 403)

        #quere database fro username
        rows = db.execute("SELECT * FROM users WHERE username = ? ", request.form.get("username"))
        #ensure that username exist and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)
        
        #remember which user logged in
        session["user_id"] = rows[0]["user_id"]
        #redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")
#log out
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/") 

#Adding new content page
@app.route("/adding", methods=["GET","POST"])
@login_required
def adding():
    if request.method == "POST":
        if not request.form.get("app_name"):
            return apology("Must provide the App name")
        elif not request.form.get("login"):
            return apology("Must provide Login")
        elif not request.form.get("password"):
            return apology("Must provide a password")
        #prepare the variables
        app_name = request.form.get("app_name")
        login = request.form.get("login")
        password = request.form.get("app_name")
        additional = request.form.get("additional")
        #hash password in db
        hash = generate_password_hash(password,method="pbkdf2:sha256")
        db.execute("INSERT INTO apps (app_id, app_name, login, password, additional) VALUES (?,?,?,?,?)",session["user_id"],app_name,login,hash,additional)
        return redirect("/")
    else:
        return render_template("adding.html")


#export FLASK_DEBUG=