# PowerShell script to run Streamlit app from the 'app' directory

Write-Host "Starting Streamlit app..."
cd app
streamlit run frontend/streamlit_app.py
