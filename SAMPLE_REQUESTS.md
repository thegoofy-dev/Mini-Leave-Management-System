-----

# SAMPLE\_REQUESTS.md

This file provides example `curl` commands for testing the Leave Management API. These commands are based on the API documentation and are intended for a local setup where the server is running on `http://127.0.0.1:5000`.

## 1\) Health Check

A simple GET request to check if the API is running.

```bash
curl http://127.0.0.1:5000/health
```

## 2\) Create Employee

A POST request to create a new employee. You will need to provide the employee's `name`, `email`, `department`, and `joining_date`.

```bash
curl -X POST http://127.0.0.1:5000/employees \
-H "Content-Type: application/json" \
-d '{
    "name": "Pankaj Tyagi",
    "email": "pankaj@example.com",
    "department": "Engineering",
    "joining_date": "2024-08-01"
}'
```

## 3\) Get Leave Balance

A GET request to retrieve the leave balance for a specific employee, identified by their `id`.

```bash
# Replace {id} with the actual employee ID
curl http://127.0.0.1:5000/employees/1/balance
```

## 4\) Apply for Leave

A POST request to submit a new leave application. Ensure the `employee_id` exists and the dates are valid.

```bash
curl -X POST http://127.0.0.1:5000/leaves \
-H "Content-Type: application/json" \
-d '{
    "employee_id": 1,
    "start_date": "2024-09-01",
    "end_date": "2024-09-03",
    "reason": "Vacation"
}'
```

## 5\) Approve Leave

A POST request to approve a pending leave request, identified by its `leave_id`.

```bash
# Replace {leave_id} with the actual leave ID
curl -X POST http://127.0.0.1:5000/leaves/1/approve
```

## 6\) Reject Leave

A POST request to reject a pending leave request, identified by its `leave_id`. An optional `reason` can be included in the body.

```bash
# Replace {leave_id} with the actual leave ID
curl -X POST http://127.0.0.1:5000/leaves/1/reject \
-H "Content-Type: application/json" \
-d '{"reason": "Conflict with project deadline"}'
```

## 7\) List Leaves for Employee

A GET request to retrieve all leave applications for a specific employee.

```bash
# Replace {id} with the actual employee ID
curl http://127.0.0.1:5000/employees/1/leaves
```