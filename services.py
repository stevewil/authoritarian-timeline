import os
import gspread
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

def get_sheet_connection():
    """
    Establishes a connection to the Google Sheet using service account credentials.
    Credentials are automatically found from the GOOGLE_APPLICATION_CREDENTIALS
    environment variable.
    """
    try:
        gc = gspread.service_account()
        sheet_id = os.getenv("GOOGLE_SHEET_ID")
        if not sheet_id:
            raise ValueError("GOOGLE_SHEET_ID environment variable not set.")
        spreadsheet = gc.open_by_key(sheet_id)
        return spreadsheet
    except Exception as e:
        print(f"Error connecting to Google Sheets: {e}")
        raise

def test_sheet_write(spreadsheet: gspread.Spreadsheet, value: str):
    """Writes a value to cell A1 of a sheet named 'Test'."""
    test_sheet = spreadsheet.worksheet("Test")
    test_sheet.update_acell("A1", value)