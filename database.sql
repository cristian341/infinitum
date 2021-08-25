CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE user_data (
    firstname TEXT NOT NULL,
    surname TEXT NOT NULL,
    email TEXT NOT NULL,
    data_id INTEGER,
    FOREIGN KEY (data_id) REFERENCES users (user_id)
);

CREATE TABLE apps (
    app_id INTEGER NOT NULL,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_name TEXT NOT NULL,
    login TEXT NOT NULL,
    password TEXT NOT NULL,
    additional TEXT
);

