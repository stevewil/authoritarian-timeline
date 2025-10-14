import gspread
import os
import sys
import traceback
from dotenv import load_dotenv
from datetime import datetime

print("--- Starting Standalone Connection Test ---")

# 1. Load Environment Variables
load_dotenv()
print("DEBUG: .env file loaded.")

creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
sheet_name = os.getenv("GOOGLE_SHEET_NAME")

if not creds_path or not sheet_name:
    print("ERROR: GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_SHEET_NAME not set in .env file.")
    sys.exit(1)

print(f"DEBUG: Credentials Path: {creds_path}")
print(f"DEBUG: Sheet Name: {sheet_name}")

try:
    # 2. Authenticate and Connect
    print(f"[{datetime.now()}] DEBUG: Authenticating with gspread...")
    gc = gspread.service_account(filename=creds_path)
    gc.http_client.timeout = 15 # Set a 15-second timeout
    print(f"[{datetime.now()}] DEBUG: Authentication successful. Opening spreadsheet...")

    # This step uses the Google Drive API to find the sheet by its title.
    spreadsheet = gc.open(sheet_name)
    print(f"[{datetime.now()}] SUCCESS: Successfully opened spreadsheet '{spreadsheet.title}'")

    # 3. Test reading from a worksheet
    # This step uses the Google Sheets API to access a specific worksheet (tab).
    print(f"[{datetime.now()}] DEBUG: Attempting to open 'LEADERS' worksheet...")
    leaders_sheet = spreadsheet.worksheet("LEADERS")
    print(f"[{datetime.now()}] DEBUG: Successfully opened 'LEADERS' worksheet. Reading first row...")
    # This step uses the Google Sheets API to read data from the cells.
    first_row = leaders_sheet.row_values(1)
    print(f"[{datetime.now()}] SUCCESS: Read first row: {first_row}")

except Exception as e:
    print(f"\n--- AN ERROR OCCURRED ---")
    traceback.print_exc()
    sys.exit(1)