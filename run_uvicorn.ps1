# PowerShell script to run Uvicorn server from the root directory

Write-Host "Starting Uvicorn server..."
uvicorn app.api.main:app --host 127.0.0.1 --port 8000 --reload
