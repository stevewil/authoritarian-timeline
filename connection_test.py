import gspread
import os
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
    exit()

print(f"DEBUG: Credentials Path: {creds_path}")
print(f"DEBUG: Sheet Name: {sheet_name}")

try:
    # 2. Authenticate and Connect
    print(f"[{datetime.now()}] DEBUG: Authenticating with gspread...")
    gc = gspread.service_account(filename=creds_path)
    gc.http_client.timeout = 15 # Set a 15-second timeout
    print(f"[{datetime.now()}] DEBUG: Authentication successful. Opening spreadsheet...")

    spreadsheet = gc.open(sheet_name)
    print(f"[{datetime.now()}] SUCCESS: Successfully opened spreadsheet '{spreadsheet.title}'")

except Exception as e:
    print(f"\n--- AN ERROR OCCURRED ---")
    import traceback
    traceback.print_exc()