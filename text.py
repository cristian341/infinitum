from cs50 import SQL

db  = SQL("sqlite:///manager.db")
rows = db.execute("SELECT password FROM users WHERE user_id = ? ",1)
            #ensure that username exist and password is correct
print(rows)
#if len(rows) != 1 or not check_password_hash(rows["password"], request.form.get("password")):
                #return apology("Invalid  password", 403)

 