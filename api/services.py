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
    # Explicitly get the path to the credentials file from the environment variable.
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    # Provide a clear error if the environment variable is not set.
    if not creds_path:
        raise ValueError(
            "The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set. "
            "Please check your .env file and ensure it points to your JSON credentials file."
        )

    # Provide a clear error if the file path itself is wrong.
    if not os.path.exists(creds_path):
        raise FileNotFoundError(
            f"The credentials file was not found at the path specified by "
            f"GOOGLE_APPLICATION_CREDENTIALS: {creds_path}"
        )

    gc = gspread.service_account(filename=creds_path)

    # Set a timeout on the underlying HTTP client to prevent indefinite hangs.
    # If a request takes longer than 15 seconds, it will raise an exception.
    gc.http_client.timeout = 15
    
    print(f"[{datetime.now()}] DEBUG: Opening spreadsheet by name: '{SHEET_NAME}'...")
    spreadsheet = gc.open(SHEET_NAME)
    print(f"[{datetime.now()}] DEBUG: Spreadsheet opened successfully.")
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

def test_leaders_read(spreadsheet: gspread.Spreadsheet):
    """
    Reads and returns the first five records from the 'Leaders' worksheet.
    """
    print(f"[{datetime.now()}] DEBUG: Fetching 'Leaders' worksheet for test read...")
    leaders_sheet = spreadsheet.worksheet("Leaders") # This is a network request
    print(f"[{datetime.now()}] DEBUG: 'Leaders' worksheet fetched. Now reading records...")
    # get_all_records() fetches all rows; we slice the first 5 records from the result.
    records = leaders_sheet.get_all_records()[:5] # This is a network request
    print(f"[{datetime.now()}] DEBUG: Successfully read {len(records)} records from 'Leaders' sheet.")
    return records

def get_timelines_data(spreadsheet: gspread.Spreadsheet):
    """
    Fetches leader and event data from the Google Sheet and processes it
    into the required JSON structure for the API.
    """
    debug_log = ["Starting timeline data processing."]

    # 1. Fetch all data from both sheets
    try:
        print(f"[{datetime.now()}] DEBUG: Fetching 'Leaders' worksheet...")
        leaders_sheet = spreadsheet.worksheet("Leaders")
        print(f"[{datetime.now()}] DEBUG: 'Leaders' worksheet fetched.")
        debug_log.append("Fetching 'Leaders' worksheet successful.")
        
        print(f"[{datetime.now()}] DEBUG: Fetching 'Events' worksheet...")
        events_sheet = spreadsheet.worksheet("Events")
        print(f"[{datetime.now()}] DEBUG: 'Events' worksheet fetched.")
        debug_log.append("Fetching 'Events' worksheet successful.")
    except gspread.exceptions.WorksheetNotFound as e:
        # This is a critical error, so we should stop and raise it.
        # The flask route will catch this and return a 500 error.
        error_msg = (
            f"CRITICAL: A required worksheet was not found: {e}. "
            "Please ensure your Google Sheet has worksheets named 'Leaders' and 'Events'."
        )
        debug_log.append(error_msg)
        raise gspread.exceptions.WorksheetNotFound(error_msg) from e

    print(f"[{datetime.now()}] DEBUG: Reading all records from 'Leaders' sheet...")
    leaders_data = leaders_sheet.get_all_records() # Returns a list of dicts
    print(f"[{datetime.now()}] DEBUG: Reading all records from 'Events' sheet...")
    events_data = events_sheet.get_all_records()   # Returns a list of dicts
    print(f"[{datetime.now()}] DEBUG: Finished reading all records.")
    debug_log.append(f"Read {len(leaders_data)} leaders and {len(events_data)} events from sheets.")
    
    # 2. Process events and group them by LeaderID for efficient lookup
    events_by_leader = {}
    for event in events_data:
        leader_id = event.get("LeaderID")
        if not leader_id:
            debug_log.append(f"Warning: Skipping an event because it has no LeaderID. Event data: {event}")
            continue

        if leader_id not in events_by_leader:
            events_by_leader[leader_id] = []
        
        events_by_leader[leader_id].append(event)

    debug_log.append("Starting to build final response structure for each leader.")
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
            warning_msg = f"Warning: Skipping leader '{leader_id}' due to invalid or missing DateAssumedPower: '{date_assumed_power_str}'"
            debug_log.append(warning_msg)
            print(warning_msg) # Also print to server console for visibility
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
                warning_msg = f"Warning: Skipping event for leader '{leader_id}' due to invalid or missing EventDate: '{event.get('EventDate')}'"
                debug_log.append(warning_msg)
                print(warning_msg) # Also print to server console
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

    debug_log.append("Finished processing all leaders.")
    return {
        "data": timelines,
        "_debug_log": debug_log
    }