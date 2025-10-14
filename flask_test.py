import datetime
import sys
import os
from flask import Flask, jsonify

# Add the project root to the Python path to ensure modules are found
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from api.services import get_sheet_connection, test_sheet_write, test_sheet_read

app = Flask(__name__)

@app.route("/")
def index():
    """A simple root route to confirm the app is running."""
    return jsonify({"message": "Authoritarian Timeline API is running."})

@app.route("/api/test-write", methods=['POST'])
def test_write():
    """Tests writing a value to the Google Sheet."""
    try:
        spreadsheet = get_sheet_connection()
        timestamp = f"Flask write successful at: {datetime.datetime.utcnow().isoformat()}"
        test_sheet_write(spreadsheet, timestamp)
        return jsonify({
            "status": "success",
            "message": f"Successfully wrote to sheet. Value: '{timestamp}'"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/test-read", methods=['GET'])
def test_read():
    """Tests reading a value from the Google Sheet."""
    try:
        spreadsheet = get_sheet_connection()
        value = test_sheet_read(spreadsheet)
        return jsonify({
            "status": "success",
            "message": f"Successfully read from sheet. Value in A1: '{value}'"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # To run for local development: `python flask_test.py`
    # Or if renamed: `python app.py`
    app.run(debug=True, port=8000)