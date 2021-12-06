import os 
#from cs50 import SQL
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from flask.helpers import get_flashed_messages
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import time
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

#connect the sqlite3 db
connection = sqlite3.connect("v2.db", check_same_thread=False)

#the home page
@app.route("/")
@login_required
def index():
    #apps= db.execute("SELECT * FROM apps WHERE app_id = ?", session["user_id"])
    cursor = connection.execute("SELECT * FROM apps WHERE app_id = ?", [session["user_id"]])
    apps = cursor.fetchall()
    return render_template("index.html",apps=apps)

# registration page
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        surname = request.form.get("surname")
        email = request.form.get("email")
        
        #error checking
        rows = cursor.execute("SELECT * FROM users WHERE username = ?", [username])
        connection.commit()
        if not username:
            #return apology("Must provide username", 400)
            flash("Must provide username")
        elif len(rows) != 0:
            #return apology("Username already exist", 400)
            flash("Username already exist")
        elif not password:
            #return apology("Must provide password", 400)
            flash("Must provide password")
        elif not confirmation:
            #return apology("Must provide a confirmation password", 400)
            flash("Must provide a confirmation password")
        elif not password == confirmation:
            return apology("Passwords must match", 400)
            
        else: 
            # generate hash of the password
            hash = generate_password_hash(password,method="pbkdf2:sha256")
            #insert new user
            #db.execute("INSERT INTO users (username,firstname,surname,password,email) VALUES (?,?,?,?,?)",username,firstname,surname,hash,email)
            cursor.executemany("INSERT INTO users (username,firstname,surname,password,email) VALUES (?,?,?,?,?)",username,firstname,surname,hash,email)
            connection.commit()
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
            #return apology("You must provide your username", 403)
            flash("You must provide your username")
        elif not request.form.get("password"):
            flash("You must provide a password")
            return apology("You must provide a password", 403)
            
        #quere database for username
        user = request.form.get("username")
        #getting data from database 
        cursor = connection.execute("SELECT * FROM users WHERE username = ? ", [user])
        product = cursor.fetchall()
        #ensure that username exist and password is correct
        if len(product) != 1 or not check_password_hash(product[0][4], request.form.get("password")):
            return apology("Invalid username and/or password", 403)
        
        #remember which user logged in
        session["user_id"] = product[0][0]
        #redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")
#log out
@app.route("/logout")
def logout():
    session.clear()
    connection.close()
    return redirect(url_for("login")) 

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
        elif  request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords must match", 400)
        #prepare the variables
        app_name = request.form.get("app_name")
        login = request.form.get("login")
        password = request.form.get("password")
        additional = request.form.get("additional")
        #db.execute("INSERT INTO apps (app_id, app_name, login, password, additional) VALUES (?,?,?,?,?)",session["user_id"],app_name,login,password,additional)
        cursor.executemany("INSERT INTO apps (app_id, app_name, login, password, additional) VALUES (?,?,?,?,?)",session["user_id"],app_name,login,password,additional)
        connection.commit()
        return redirect("/")
    else:
        return render_template("adding.html")

@app.route("/find")
def find():
    return render_template("find.html")

#search the app
@app.route("/search")
def search():
    #q = request.args.get("q")
    #if q:
      #  apps = db.execute("SELECT * FROM apps WHERE app_name LIKE ? AND app_id = ?", "%" + q + "%", session["user_id"])
    #else:
      #  apps = []
    #return render_template("search.html", apps=apps)
    pass

#update the app information
@app.route("/update", methods=["GET","POST"])
@login_required
def update():
    if request.method == "POST":
        #checking if the id is correct
        id_in = int(request.form.get("id"))
        #v = db.execute("SELECT id FROM apps WHERE app_id = ?", session["user_id"])
        v = cursor.execute("SELECT id FROM apps WHERE app_id = ?", session["user_id"])
        id = []
        for app in v:
            id.append(app["id"])
        if id_in in id:
            login = request.form.get("login")
            password = request.form.get("password")
            confiramtion = request.form.get("confirmation")
            additional = request.form.get("additonal")

            if not login:
                return apology("Must provide the Login", 400)
            elif not password or not confiramtion:
                return apology("Must provide password", 400)
            elif password != confiramtion:
                return apology("Password does not much", 400)
            if additional is None:
                #db.execute("UPDATE apps SET  login=?, password=? WHERE id = ? AND app_id = ?",login,password,id_in, session["user_id"])
                cursor.executemany("UPDATE apps SET  login=?, password=? WHERE id = ? AND app_id = ?",login,password,id_in, session["user_id"])
                connection.commit()
                flash("Successful")
            else:
                #db.execute("UPDATE apps SET  login=?, password=?, additional=? WHERE id = ? AND app_id = ?",login,password,additional,id_in, session["user_id"])
                cursor.executemany("UPDATE apps SET  login=?, password=?, additional=? WHERE id = ? AND app_id = ?",login,password,additional,id_in, session["user_id"])
                connection.commit()
                flash("Successful")
            return redirect("/")
        else:
            return apology("ID not found", 400)
    else:
        return render_template("update.html")

#delete app 
@app.route("/delete",methods=["GET","POST"])
@login_required
def delete():
    if request.method == "POST":
        id_in = int(request.form.get("id"))
        #v = db.execute("SELECT id FROM apps WHERE app_id = ?", session["user_id"])
        v = cursor.execute("SELECT id FROM apps WHERE app_id = ?", session["user_id"])
        id = []
        for app in v:
            id.append(app["id"])
        if id_in in id:
            #rows = db.execute("SELECT password FROM users WHERE user_id = ? ", session["user_id"])
            rows = cursor.executemany("SELECT password FROM users WHERE user_id = ? ", session["user_id"])
            if int(len(rows)) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
                return apology("Invalid  password", 403)
            #db.execute("DELETE FROM apps WHERE id = ?", id_in)
            cursor.execute("DELETE FROM apps WHERE id = ?", id_in)
            connection.commit()
            flash("Success")
            return redirect("/")
        else:
            return apology("Invalid ID",400)
    else:
        return render_template("delete.html")



