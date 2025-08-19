# High Level Design (HLD)

## Architecture (Mermaid)
```mermaid
graph LR
  A[Frontend (React / Minimal UI)] --> B[Backend (Flask API)]
  B --> C[(SQLite / RDBMS)]
  B --> D[Auth Service (future)]
  B --> E[Notification Service (email/slack) - future]
```

## Notes on scaling
- Move from SQLite to PostgreSQL/MySQL for concurrency.
- Use connection pooling and deploy backend instances behind a load balancer.
- Use Redis for caching frequently requested data.
- Add background workers for notifications and reports.