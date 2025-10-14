import datetime
import sys
import os
from flask import Flask, jsonify
import traceback

# Add the project root to the Python path to ensure modules are found
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from api.services import get_sheet_connection, test_sheet_write, test_sheet_read, get_timelines_data

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
        timestamp = f"Flask write successful at: {datetime.datetime.utcnow().isoformat()}"
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