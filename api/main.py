from fastapi import FastAPI, HTTPException
from . import services
import datetime

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Authoritarian Timeline API is running."}

@app.post("/api/test-write", status_code=200)
def test_google_sheet_write():
    """
    A test endpoint to confirm write permissions to the Google Sheet.
    It writes the current timestamp to cell A1 of the 'Test' worksheet.
    """
    try:
        spreadsheet = services.get_sheet_connection()
        timestamp = f"Write successful at: {datetime.datetime.utcnow().isoformat()}"
        services.test_sheet_write(spreadsheet, timestamp)
        return {"status": "success", "message": f"Successfully wrote to sheet. Value: '{timestamp}'"}
    except Exception as e:
        # Raise an HTTP exception to provide a clear error response in the API
        raise HTTPException(status_code=500, detail=f"Failed to write to Google Sheet: {str(e)}")

@app.get("/api/test-read", status_code=200)
def test_google_sheet_read():
    """
    A test endpoint to confirm read permissions from the Google Sheet.
    It reads the value from cell A1 of the 'Test' worksheet.
    """
    try:
        spreadsheet = services.get_sheet_connection()
        value = services.test_sheet_read(spreadsheet)
        return {"status": "success", "message": f"Successfully read from sheet. Value in A1: '{value}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read from Google Sheet: {str(e)}")