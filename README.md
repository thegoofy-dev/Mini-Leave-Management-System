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