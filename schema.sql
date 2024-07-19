CREATE TABLE IF NOT EXISTS user (
    id        TEXT PRIMARY KEY,
    hash      TEXT,
    role      TEXT);

CREATE TABLE IF NOT EXISTS exercise (
    user_id   TEXT,
    mod       INTEGER,
    num       INTEGER,
    grade     INTEGER,
    period    TEXT,
    details   TEXT,
    FOREIGN KEY(user_id)   REFERENCES user(id));

