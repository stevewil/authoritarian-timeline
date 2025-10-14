import gspread
import os
from dotenv import load_dotenv
from datetime import datetime

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

def get_timelines_data():
    """
    Fetches leader and event data from the Google Sheet and processes it
    into the required JSON structure for the API.
    """
    print("DEBUG: Attempting to connect to Google Sheets...")
    spreadsheet = get_sheet_connection()
    print("DEBUG: Connection successful.")

    # 1. Fetch all data from both sheets
    print("DEBUG: Fetching 'Leaders' worksheet...")
    leaders_sheet = spreadsheet.worksheet("Leaders")
    print("DEBUG: Fetching 'Events' worksheet...")
    events_sheet = spreadsheet.worksheet("Events")
    
    print("DEBUG: Reading all records from sheets...")
    leaders_data = leaders_sheet.get_all_records() # Returns a list of dicts
    events_data = events_sheet.get_all_records()   # Returns a list of dicts
    print(f"DEBUG: Found {len(leaders_data)} leaders and {len(events_data)} events.")
    
    # 2. Process events and group them by LeaderID for efficient lookup
    events_by_leader = {}
    for event in events_data:
        leader_id = event.get("LeaderID")
        if not leader_id:
            continue # Skip events without a leader ID

        if leader_id not in events_by_leader:
            events_by_leader[leader_id] = []
        
        events_by_leader[leader_id].append(event)

    print("DEBUG: Starting to build final response structure...")
    # 3. Build the final response structure
    timelines = []
    for leader in leaders_data:
        leader_id = leader.get("LeaderID")
        if not leader_id:
            continue # Skip leaders without an ID

        # Parse the "zero point" date
        try:
            date_assumed_power_str = leader.get("DateAssumedPower")
            date_assumed_power = datetime.strptime(date_assumed_power_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            # Skip leader if the date is invalid or missing
            print(f"Warning: Skipping leader '{leader_id}' due to invalid DateAssumedPower: '{date_assumed_power_str}'")
            continue

        leader_events = []
        for event in events_by_leader.get(leader_id, []):
            try:
                event_date_str = event.get("EventDate")
                event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
                days_diff = (event_date - date_assumed_power).days

                leader_events.append({
                    "EventDate": event.get("EventDate"),
                    "EventTitle": event.get("EventTitle"),
                    "days_from_start": days_diff
                })
            except (ValueError, TypeError):
                print(f"Warning: Skipping event for leader '{leader_id}' due to invalid EventDate: '{event.get('EventDate')}'")
                continue
        
        timelines.append({
            "details": {
                "LeaderID": leader.get("LeaderID"),
                "FullName": leader.get("FullName"),
                "Country": leader.get("Country"),
                "DateAssumedPower": leader.get("DateAssumedPower"),
                "Color": leader.get("Color")
            },
            "events": sorted(leader_events, key=lambda x: x['days_from_start'])
        })

    print("DEBUG: Finished processing. Returning timelines.")
    return timelines