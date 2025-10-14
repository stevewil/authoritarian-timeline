import gspread
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# It's best practice to load the sheet name from an environment variable
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Authoritarian Timeline Data")

def get_sheet_connection():
    """
    Establishes a connection to the Google Sheet using service account credentials.
    """
    # The gspread.service_account() function automatically looks for the
    # GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # Ensure your .env file sets this to the path of your JSON credentials file.
    gc = gspread.service_account()
    spreadsheet = gc.open(SHEET_NAME)
    return spreadsheet

def test_sheet_write(spreadsheet: gspread.Spreadsheet, value: str):
    """
    Writes a given value to cell A1 of the 'Test' worksheet.
    """
    test_worksheet = spreadsheet.worksheet("Test")
    test_worksheet.update_acell("A1", value)

def test_sheet_read(spreadsheet: gspread.Spreadsheet) -> str:
    """
    Reads the value from cell A1 of the 'Test' worksheet.
    """
    test_worksheet = spreadsheet.worksheet("Test")
    return test_worksheet.acell("A1").value