# Mini Leave Management System — Step-by-step scaffold

This repository is a step-by-step scaffold of a simple Leave Management System (Flask + SQLite).

## Quick start (local)

1. Create virtualenv and activate:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Visit health:
   ```bash
   curl http://127.0.0.1:5000/health
   ```

## Files
- `app.py` — Flask API
- `models.py` — SQLite models
- `requirements.txt`
- `SAMPLE_REQUESTS.md` — curl examples
- `HLD.md` — high-level design

## Notes
- Default leave balance: 18 days
- Dates format: YYYY-MM-DD

## Contents
This ZIP includes:
- Source code (Flask + SQLite): `app.py`, `models.py`
- README (this file)
- API docs: `API_DOCS.md` (endpoints, sample input/output)
- High Level Design: `HLD.md` (mermaid diagrams + class pseudocode)
- APIDOG collection: `apidog_collection.json` (importable)
- Sample outputs: `samples/` (curl response examples)
- Setup script: `run_seed.sh` to seed sample data

---

## Setup steps (local)
1. Unzip the project and open in VS Code.
2. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate   # Windows: .\venv\Scripts\activate

   pip install -r requirements.txt
   python app.py
   bash run_seed.sh
   [http://127.0.0.1:5000](http://127.0.0.1:5000)
    ```

3. Assumptions
- Each new employee receives 18 leave days by default.
- Leaves are full-day only and inclusive of start and end dates.
- No authentication (HR actions are unauthenticated for MVP).
- No holiday calendar (holidays are not auto-blocked).
- No carry-forward or accrual policy implemented.


4. Edge cases handled
- Applying for leave before joining date.
- Applying for more days than available balance.
- Overlapping leave requests (PENDING or APPROVED).
- Employee not found.
- Invalid dates (end date before start date).
- Duplicate employee email on creation.
- Prevent approving/rejecting non-pending leaves.
- Check balance again at approval time (prevents race).

5. Potential improvements
- Add authentication (JWT) and role-based access (employee vs HR).
- Move to PostgreSQL/MySQL and deploy with Gunicorn + Nginx.
- Add public holiday calendar and half-day leaves.
- Implement monthly accrual and carry-forward rules.
- Add UI (React) and pagination/filtering for lists.
- Add unit & integration tests and CI/CD pipeline.

**GitHub Repo Link**: https://github.com/thegoofy-dev/Mini-Leave-Management-System/

**Live Link**: https://mini-leave-management-system-pcvl.onrender.com/
---