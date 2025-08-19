# Sample curl requests

# Create employee
curl -X POST http://127.0.0.1:5000/employees -H "Content-Type: application/json" -d '{
  "name":"Test User",
  "email":"demo@example.com",
  "department":"Engineering",
  "joining_date":"2024-08-01"
}'

# Apply leave
curl -X POST http://127.0.0.1:5000/leaves -H "Content-Type: application/json" -d '{
  "employee_id":1,
  "start_date":"2024-09-01",
  "end_date":"2024-09-03",
  "reason":"Trip"
}'

# Approve leave
curl -X POST http://127.0.0.1:5000/leaves/1/approve

# Reject leave
curl -X POST http://127.0.0.1:5000/leaves/1/reject -H "Content-Type: application/json" -d '{"reason":"Conflict"}'

# Get balance
curl http://127.0.0.1:5000/employees/1/balance

# List leaves
curl http://127.0.0.1:5000/employees/1/leaves