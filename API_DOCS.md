### **API_DOCS.md**

# API_DOCS

Base URL: http://127.0.0.1:5000

## 1) Health
`GET /health`

Response:
```
{
  "status": "ok"
}
```
### 2) Root

`GET /`

Response:
```
{
  "message": "Leave Management API Running 🚀"
}
```

## 3) Create employee

`POST /employees`

Body (JSON):
```
{
  "name": "Test User",
  "email": "demo@example.com",
  "department": "Engineering",
  "joining_date": "2024-08-01"
}
```

Success (201):
```
{
  "id": 1,
  "name": "Test User",
  "email": "demo@example.com",
  "department": "Engineering",
  "joining_date": "2024-08-01",
  "leave_balance": 18
}
```
Errors:
  -  400 if missing fields or invalid date.
  -  409 if duplicate email.

## 4) Get leave balance

`GET /employees/{id}/balance`

Success:
```
{
  "id": 1,
  "leave_balance": 18
}
```

Error: 404 if employee not found.

## 5) Apply leave

`POST /leaves`
Body(JSON) :

```
{
  "employee_id": 1,
  "start_date": "2024-09-01",
  "end_date": "2024-09-03",
  "reason": "Vacation"
}
```

Success (201):
```
{
  "id": 1,
  "employee_id": 1,
  "start_date": "2024-09-01",
  "end_date": "2024-09-03",
  "reason": "Vacation",
  "status": "PENDING",
  "rejection_reason": null,
  "created_at": "2024-08-19 12:00:00"
}
```
Errors:
  -  400 invalid dates / insufficient balance
  -  409 overlapping leave exists

## 6) Approve leave

`POST /leaves/{leave_id}/approve`

```
Success:
{
  "id": 1,
  "status": "APPROVED",
  "employee_leave_balance": 15
}
```

Errors:
  -  404 leave not found
  -  400 only pending leaves can be approved
  -  400 insufficient balance at approval time

## 7) Reject leave

`POST /leaves/{leave_id}/reject`

Body (optional):
```
{"reason": "Conflict"}
```
Success:
```
{
  "id": 1,
  "status": "REJECTED"
}
```

## 8) List leaves for employee

`GET /employees/{id}/leaves`

Response:
```
{
  "employee": { ... },
  "leaves": [ ... ]
}
```

---