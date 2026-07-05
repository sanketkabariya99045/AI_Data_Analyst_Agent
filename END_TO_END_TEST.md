
# End-to-End Test

1. Start FastAPI:
   uvicorn api.main:app --reload

2. Start Streamlit:
   streamlit run frontend/app.py

3. Upload:
   - CSV
   - XLSX
   - Multiple files

Expected:
- Success message
- JSON response
- Preview tables
- Metadata returned by backend
- Logs written to logs/app.log
