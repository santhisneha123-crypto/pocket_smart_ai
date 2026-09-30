# PocketSmart AI

A budget-planning app with a FastAPI backend and a standalone HTML frontend.

## Features

- Compare estimated recommendation costs with the budget and view category allocations.
- Save and reload up to 30 plans in this browser.
- Download a plan as JSON or print it / save it as PDF from the browser.
- Search recommended products on the relevant retailer site.

## Project files

- `backend/main.py`: serves the frontend and provides recommendation and outfit-upload APIs.
- `frontend/index.html`: browser interface.
- `backend/__init__.py`: marks the backend as an importable Python package.
- `.env`: local configuration; keep API keys here and do not commit this file.
- `.env.example`: environment-variable template.
- `requirements.txt`: Python dependencies.

## Setup on Windows

1. Create and activate a virtual environment:

   ```powershell
   & "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Add your Gemini API key to `.env` to enable AI recommendations:

   ```text
   GEMINI_API_KEY=your_api_key_here
   ```

   If the key is blank or missing, the app returns built-in demo recommendations.

4. Start the app:

   ```powershell
   python -m uvicorn backend.main:app --reload
   ```

5. Open <http://127.0.0.1:8000> in your browser. Interactive API documentation is available at <http://127.0.0.1:8000/docs>.

## API

- `POST /recommend`: accepts a planner, budget, and requirements; returns recommendations.
Saved plans remain in the current browser and are not uploaded to the server.
