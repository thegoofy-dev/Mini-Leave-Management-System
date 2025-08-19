from flask import Flask, request, jsonify
from datetime import datetime
from models import init_db, get_db, Employee, LeaveRequest
import os

DB_PATH = os.environ.get("DB_PATH", "leave_mgmt.db")

app = Flask(__name__)
init_db(DB_PATH)

def parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None

@app.route("/")
def home():
    return """
    <h1>🚀 Mini Leave Management System</h1>
    <p>Welcome! Use the links below to explore the API:</p>
    <ul>
        <li><a href="/health">Health Check</a></li>
        <li><a href="/employees/1/balance">Check Employee Leave Balance (example)</a></li>
        <li><a href="/employees/1/leaves">List Leaves for Employee (example)</a></li>
    </ul>
    <p>⚠️ Note: Some routes require POST requests with JSON (e.g., /employees, /leaves). Use Postman/APIDog to test those.</p>
    """

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok"})

@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    department = data.get("department","")
    joining_date_s = data.get("joining_date")
    if not (name and email and joining_date_s):
        return jsonify({"error":"name, email and joining_date are required (YYYY-MM-DD)"}),400
    joining_date = parse_date(joining_date_s)
    if not joining_date:
        return jsonify({"error":"invalid joining_date format, use YYYY-MM-DD"}),400
    db = get_db(DB_PATH)
    if Employee.find_by_email(db, email):
        return jsonify({"error":"employee with this email already exists"}),409
    emp = Employee.create(db, name, email, department, joining_date.isoformat())
    return jsonify(emp),201

@app.route("/employees/<int:emp_id>/balance", methods=["GET"])
def get_balance(emp_id):
    db = get_db(DB_PATH)
    emp = Employee.find_by_id(db, emp_id)
    if not emp:
        return jsonify({"error":"employee not found"}),404
    return jsonify({"id": emp["id"], "leave_balance": emp["leave_balance"]})

@app.route("/leaves", methods=["POST"])
def apply_leave():
    data = request.get_json() or {}
    emp_id = data.get("employee_id")
    start_s = data.get("start_date")
    end_s = data.get("end_date")
    reason = data.get("reason","")
    if not (emp_id and start_s and end_s):
        return jsonify({"error":"employee_id, start_date, end_date required (YYYY-MM-DD)"}),400
    start = parse_date(start_s)
    end = parse_date(end_s)
    if not start or not end:
        return jsonify({"error":"invalid date format, use YYYY-MM-DD"}),400
    if end < start:
        return jsonify({"error":"end_date cannot be before start_date"}),400
    db = get_db(DB_PATH)
    emp = Employee.find_by_id(db, emp_id)
    if not emp:
        return jsonify({"error":"employee not found"}),404
    jdate = datetime.strptime(emp["joining_date"], "%Y-%m-%d").date()
    if start < jdate:
        return jsonify({"error":"cannot apply leave before joining date"}),400
    days = (end - start).days + 1
    overlapping = LeaveRequest.find_overlapping(db, emp_id, start.isoformat(), end.isoformat())
    if overlapping:
        return jsonify({"error":"overlapping leave exists", "overlap_count": len(overlapping)}),409
    if days > emp["leave_balance"]:
        return jsonify({"error":"insufficient leave balance", "requested_days": days, "available": emp["leave_balance"]}),400
    lr = LeaveRequest.create(db, emp_id, start.isoformat(), end.isoformat(), reason)
    return jsonify(lr),201

@app.route("/leaves/<int:leave_id>/approve", methods=["POST"])
def approve_leave(leave_id):
    db = get_db(DB_PATH)
    lr = LeaveRequest.find_by_id(db, leave_id)
    if not lr:
        return jsonify({"error":"leave not found"}),404
    if lr["status"] != "PENDING":
        return jsonify({"error":"only pending leaves can be approved"}),400
    emp = Employee.find_by_id(db, lr["employee_id"])
    days = (datetime.strptime(lr["end_date"], "%Y-%m-%d").date() - datetime.strptime(lr["start_date"], "%Y-%m-%d").date()).days + 1
    if days > emp["leave_balance"]:
        return jsonify({"error":"insufficient balance at approval time", "available": emp["leave_balance"], "required": days}),400
    LeaveRequest.update_status(db, leave_id, "APPROVED")
    Employee.decrement_balance(db, emp["id"], days)
    emp2 = Employee.find_by_id(db, emp["id"])
    return jsonify({"id": leave_id, "status": "APPROVED", "employee_leave_balance": emp2["leave_balance"]})

@app.route("/leaves/<int:leave_id>/reject", methods=["POST"])
def reject_leave(leave_id):
    data = request.get_json() or {}
    reason = data.get("reason","")
    db = get_db(DB_PATH)
    lr = LeaveRequest.find_by_id(db, leave_id)
    if not lr:
        return jsonify({"error":"leave not found"}),404
    if lr["status"] != "PENDING":
        return jsonify({"error":"only pending leaves can be rejected"}),400
    LeaveRequest.update_status(db, leave_id, "REJECTED", reason)
    return jsonify({"id": leave_id, "status": "REJECTED"})

@app.route("/employees/<int:emp_id>/leaves", methods=["GET"])
def list_leaves(emp_id):
    db = get_db(DB_PATH)
    emp = Employee.find_by_id(db, emp_id)
    if not emp:
        return jsonify({"error":"employee not found"}),404
    lrs = LeaveRequest.find_by_employee(db, emp_id)
    return jsonify({"employee": emp, "leaves": lrs})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))