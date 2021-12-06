import sqlite3
connection = sqlite3.connect("v2.db")
from werkzeug.security import check_password_hash, generate_password_hash

cursor = connection.execute("SELECT * FROM apps WHERE app_id = ?", [1])
apps = cursor.fetchall()
for app in apps:
    print(app[3])