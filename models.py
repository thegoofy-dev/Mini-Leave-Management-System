import sqlite3

def get_db(db_path="leave_mgmt.db"):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path="leave_mgmt_stepby_step.db"):
    db = get_db(db_path)
    c = db.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        department TEXT,
        joining_date TEXT NOT NULL,
        leave_balance INTEGER NOT NULL
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS leave_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        reason TEXT,
        status TEXT NOT NULL DEFAULT 'PENDING',
        rejection_reason TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(employee_id) REFERENCES employees(id)
    )
    """)
    db.commit()
    db.close()

class Employee:
    @staticmethod
    def create(db, name, email, department, joining_date):
        balance = 18
        cur = db.cursor()
        cur.execute("INSERT INTO employees (name,email,department,joining_date,leave_balance) VALUES (?,?,?,?,?)",
                    (name, email, department, joining_date, balance))
        db.commit()
        return Employee.find_by_id(db, cur.lastrowid)
    @staticmethod
    def find_by_email(db, email):
        cur = db.cursor()
        cur.execute("SELECT * FROM employees WHERE email = ?", (email,))
        r = cur.fetchone()
        return dict(r) if r else None
    @staticmethod
    def find_by_id(db, id):
        cur = db.cursor()
        cur.execute("SELECT * FROM employees WHERE id = ?", (id,))
        r = cur.fetchone()
        return dict(r) if r else None
    @staticmethod
    def decrement_balance(db, emp_id, days):
        cur = db.cursor()
        cur.execute("UPDATE employees SET leave_balance = leave_balance - ? WHERE id = ?", (days, emp_id))
        db.commit()

class LeaveRequest:
    @staticmethod
    def create(db, employee_id, start_date, end_date, reason):
        cur = db.cursor()
        cur.execute("INSERT INTO leave_requests (employee_id, start_date, end_date, reason) VALUES (?,?,?,?)",
                    (employee_id, start_date, end_date, reason))
        db.commit()
        return LeaveRequest.find_by_id(db, cur.lastrowid)
    @staticmethod
    def find_by_id(db, id):
        cur = db.cursor()
        cur.execute("SELECT * FROM leave_requests WHERE id = ?", (id,))
        r = cur.fetchone()
        return dict(r) if r else None
    @staticmethod
    def update_status(db, id, status, rejection_reason=None):
        cur = db.cursor()
        cur.execute("UPDATE leave_requests SET status = ?, rejection_reason = ? WHERE id = ?", (status, rejection_reason, id))
        db.commit()
        return LeaveRequest.find_by_id(db, id)
    @staticmethod
    def find_overlapping(db, employee_id, start_iso, end_iso):
        cur = db.cursor()
        cur.execute("""
        SELECT * FROM leave_requests
        WHERE employee_id = ?
          AND status IN ('PENDING','APPROVED')
          AND NOT (date(end_date) < date(?) OR date(start_date) > date(?))
        """, (employee_id, start_iso, end_iso))
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    @staticmethod
    def find_by_employee(db, employee_id):
        cur = db.cursor()
        cur.execute("SELECT * FROM leave_requests WHERE employee_id = ? ORDER BY created_at DESC", (employee_id,))
        rows = cur.fetchall()
        return [dict(r) for r in rows]