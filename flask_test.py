import datetime
from flask import Flask, jsonify

from api.services import get_sheet_connection, test_sheet_write, test_sheet_read

app = Flask(__name__)

@app.route("/")
def index():
    """A simple index route to confirm the app is running."""
    return "Flask Google Sheets Test App is running."

@app.route("/test-write", methods=['POST'])
def test_write():
    """Tests writing a value to the Google Sheet."""
    try:
        spreadsheet = get_sheet_connection()
        timestamp = f"Flask write successful at: {datetime.datetime.utcnow().isoformat()}"
        test_sheet_write(spreadsheet, timestamp)
        return jsonify({"status": "success", "message": f"Successfully wrote to sheet. Value: '{timestamp}'"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/test-read", methods=['GET'])
def test_read():
    """Tests reading a value from the Google Sheet."""
    try:
        spreadsheet = get_sheet_connection()
        value = test_sheet_read(spreadsheet)
        return jsonify({"status": "success", "message": f"Successfully read from sheet. Value in A1: '{value}'"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # To run: `python flask_test.py`
    app.run(debug=True, port=5001)