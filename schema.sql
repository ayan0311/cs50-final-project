CREATE TABLE IF NOT EXISTS users (
    id INTEGER,
    first_name TEXT NOT NULL,
    last_name TEXT,
    email TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0,
    activation_status TEXT DEFAULT 'inactive',
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS files (
    id INTEGER,
    number INTEGER NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS divisions (
    id INTEGER,
    name TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER,
    name TEXT NOT NULL,
    division_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (division_id) REFERENCES divisions(id)
);

CREATE TABLE IF NOT EXISTS file_employee_connections (
    id INTEGER,
    file_id INTEGER,
    employee_id INTEGER,
    PRIMARY KEY (id)
    FOREIGN KEY (file_id) REFERENCES file(id),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS bills (
    id INTEGER,
    file_id INTEGER,
    patient_name TEXT NOT NULL,
    patient_relation TEXT NOT NULL,
    claimed_amount INTEGER NOT NULL,
    sanctioned_amount INTEGER NOT NULL,
    bill_date DATE NOT NULL DEFAULT CURRENT_DATE,
    sanction_date DATE,
    PRIMARY KEY (id),
    FOREIGN KEY (file_id) REFERENCES files(id)
);