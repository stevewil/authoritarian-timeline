import sys
import os
from datetime import datetime
from flask import Flask, jsonify
import traceback
import json

from api.services import get_sheet_connection, test_sheet_write, test_sheet_read, test_leaders_read, get_timelines_data

app = Flask(__name__)

@app.route("/")
def index():
    """A simple root route to confirm the app is running."""
    return jsonify({"message": "Authoritarian Timeline API is running."})

@app.route("/api/test-write", methods=['POST'])
def test_write():
    """Tests writing a value to the Google Sheet."""
    try:
        # Defer connection until the request is made
        spreadsheet = get_sheet_connection()
        timestamp = f"Flask write successful at: {datetime.utcnow().isoformat()}"
        # Pass the connection to the service function
        test_sheet_write(spreadsheet, timestamp)
        return jsonify({
            "status": "success",
            "message": f"Successfully wrote to sheet. Value: '{timestamp}'"
        }), 200
    except Exception as e:
        print(f"--- ERROR IN /api/test-write ---")
        traceback.print_exc()
        print("--------------------------------")
        return jsonify({"status": "error", "message": "An internal error occurred during test write."}), 500

@app.route("/api/test-read", methods=['GET'])
def test_read():
    """Tests reading a value from the Google Sheet."""
    try:
        # Defer connection until the request is made
        spreadsheet = get_sheet_connection()
        # Pass the connection to the service function
        value = test_sheet_read(spreadsheet)
        return jsonify({
            "status": "success",
            "message": f"Successfully read from sheet. Value in A1: '{value}'"
        }), 200
    except Exception as e:
        print(f"--- ERROR IN /api/test-read ---")
        traceback.print_exc()
        print("-------------------------------")
        return jsonify({"status": "error", "message": "An internal error occurred during test read."}), 500

@app.route("/api/test-leaders-read", methods=['GET'])
def test_leaders():
    """
    A test endpoint to read and display the first 5 rows from the 'Leaders' sheet.
    """
    print("\n--- [test-leaders-read] Request Received ---")
    try:
        print(f"[{datetime.now()}] DEBUG [Route]: Attempting to get sheet connection...")
        spreadsheet = get_sheet_connection()
        print(f"[{datetime.now()}] DEBUG [Route]: Sheet connection obtained. Calling service function...")
        first_five_rows = test_leaders_read(spreadsheet)
        print(f"[{datetime.now()}] DEBUG [Route]: Service function returned successfully.")
        print("\n--- First 5 Leader Rows (Console Output) ---")
        print(json.dumps(first_five_rows, indent=2)) # Pretty print for readability
        print("------------------------------------------\n")
        return jsonify(first_five_rows), 200
    except Exception as e:
        print(f"--- ERROR IN /api/test-leaders-read ---")
        traceback.print_exc()
        print("---------------------------------------")
        return jsonify({"status": "error", "message": "An internal error occurred while reading the Leaders sheet."}), 500

@app.route("/api/timelines", methods=['GET'])
def get_timelines():
    """Fetches and returns all processed leader and event data."""
    try:
        # Best practice: Get a new connection for each request to ensure freshness
        # and handle potential connection drops gracefully.
        spreadsheet = get_sheet_connection()
        # Pass the connection to the data processing function.
        response_data = get_timelines_data(spreadsheet)
        return jsonify(response_data), 200
    except Exception as e:
        # Log the full traceback to the console for detailed debugging
        print("--- AN ERROR OCCURRED ---")
        traceback.print_exc()
        print("-------------------------")
        return jsonify({"status": "error", "message": "An internal error occurred while fetching timeline data."}), 500

if __name__ == '__main__':
    # To run for local development: `python app.py`
    app.run(debug=True, port=8000)