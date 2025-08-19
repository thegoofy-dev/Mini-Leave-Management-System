### **HLD.md**


# High Level Design (HLD)

## Architecture (Mermaid)
```
graph LR
  UX[Frontend - React/HTML] --> API[Backend - Flask API]
  API --> DB[(SQLite -> Postgres for scale)]
  API -->|Notifications| NOTIF[Worker/Notifications]
```
## Class Diagram (Mermaid)

Code snippet
``` 
classDiagram
    class Employee {
        +int id
        +string name
        +string email
        +string department
        +date joining_date
        +int leave_balance
    }
    class LeaveRequest {
        +int id
        +int employee_id
        +date start_date
        +date end_date
        +string reason
        +string status
        +string rejection_reason
    }
    Employee "1" -- "many" LeaveRequest : has
```

## Sequence (Apply leave)

Code snippet
```
sequenceDiagram
    Employee->>API: POST /leaves (start_date, end_date)
    API->>DB: validate employee, check joining_date
    API->>DB: check overlapping leaves
    API->>DB: check balance
    DB-->>API: create leave_request (PENDING)
    API-->>Employee: 201 Created
```

## Scaling notes

    For 50 -> 500 employees:

        Replace SQLite with PostgreSQL

        Add Gunicorn + Nginx, deploy behind Load Balancer

        Use Redis for caching and locks (to prevent race conditions)

        Add background workers for notifications and periodic accrual


---