# PowerShell script to activate ml_env and run Uvicorn server

Write-Host "Activating ml_env virtual environment..."
& .\\ml_env\\Scripts\\Activate.ps1

Write-Host "Starting Uvicorn server..."
uvicorn app.api.main:app --host 127.0.0.1 --port 8000 --reload
