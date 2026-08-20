CREATE TABLE IF NOT EXISTS users (
    id INTEGER,
    first_name TEXT NOT NULL,
    last_name TEXT,
    email TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT FALSE,
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

CREATE TABLE IF NOT EXISTS login_logs (
    id INTEGER,
    user_id INTEGER NOT NULL,
    logged_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    activity TEXT NOT NULL CHECK(activity IN ('login', 'logout', 'modified_pass')),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS user_logs (
    id INTEGER,
    user_id INTEGER NOT NULL,
    logged_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    activity TEXT NOT NULL CHECK(activity IN ('opened', 'deleted', 'accessed', 'modified')),
    file_id INTEGER DEFAULT 0,
    bill_id INTEGER DEFAULT 0,
    division_id INTEGER DEFAULT 0,
    employee_id INTEGER DEFAULT 0,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS admin_logs (
    id INTEGER,
    admin_id INTEGER NOT NULL,
    logged_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    activity TEXT NOT NULL CHECK(activity IN ('activated', 'suspended', 'modified', 'accessed_user_logs', 'accessed_admin_logs')),
    user_id INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);