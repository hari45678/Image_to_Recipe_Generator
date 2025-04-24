# PowerShell script to run Streamlit app and Uvicorn server from the 'app' directory

# Run Streamlit app
Write-Host "Starting Streamlit app..."
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd app; streamlit run frontend/streamlit_app.py'

# Run Uvicorn server
Write-Host "Starting Uvicorn server..."
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd app; uvicorn main:app --host 127.0.0.1 --port 8000 --reload'
