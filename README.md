# hi, mom, again and again
# Authoritarian Timeline Project

This project is a web application designed to visualize and compare the timelines of various political leaders. It uses a Python backend to fetch data from a Google Sheet and presents it as a series of stacked, interactive timeline "ribbons" on a web-based frontend.

The core concept is to normalize each leader's timeline to a "zero point"—the date they officially assumed power. This allows for a direct, year-by-year comparison of events, policies, and actions across different leadership tenures.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Data Schema (Google Sheets)](#data-schema-google-sheets)
- [Local Development Setup](#local-development-setup)
- [Backend API](#backend-api)
- [Frontend](#frontend)
- [Next Steps & Future Enhancements](#next-steps--future-enhancements)
- [Deployment](#deployment)

---

## Project Overview

The application consists of three main parts:

1.  **Data Source**: A Google Sheet acts as a simple, collaborative database to store information about leaders and the key events in their timelines.
2.  **Backend API**: A Python application built with **FastAPI** reads data from the Google Sheet, processes it into a structured JSON format, and serves it via a REST API.
3.  **Frontend Client**: A static web page (HTML, CSS, JavaScript) that fetches the data from the backend API and uses a visualization library to render the interactive timelines.

## Technology Stack

| Component      | Technology                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------------ |
| **Backend**      | [Python 3.9+](https://www.python.org/), [FastAPI](https://fastapi.tiangolo.com/)                        |
| **Data Access**  | [GSpread](https://docs.gspread.org/en/latest/) (for Google Sheets API)                                   |
| **Web Server**   | [Uvicorn](https://www.uvicorn.org/) (ASGI server for FastAPI)                                            |
| **Data Validation**| [Pydantic](https://docs.pydantic.dev/) (Integrated with FastAPI)                                       |
| **Data Source**  | [Google Sheets](https://www.google.com/sheets/about/)                                                  |
| **Frontend**     | HTML5, CSS3, JavaScript. Visualization library TBD (e.g., [Vis.js](https://visjs.org/), [D3.js](https://d3js.org/), [Apache ECharts](https://echarts.apache.org/)) |
| **Deployment**   | [Netlify](https://www.netlify.com/), [GitHub](https://github.com/)                                      |

## Project Structure

The project will follow a standard structure for a modern web application with a separate frontend and backend.

```
/
├── .gitignore
├── README.md
├── netlify.toml         # Netlify deployment and build configuration
├── requirements.txt     # Python dependencies
│
├── api/
│   ├── main.py          # The main FastAPI application logic and endpoints
│   ├── schemas.py       # Pydantic models for data validation and serialization
│   └── services.py      # Business logic for fetching/processing Google Sheet data
│
├── .env.example         # Example environment variables file
│
└── public/              # Contains all static frontend assets
    ├── index.html
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## Data Schema (Google Sheets)

The entire dataset is managed in a single Google Sheet with two tabs: `Leaders` and `Events`.

### `Leaders` Sheet

This sheet contains one row per leader.

| Column Name         | Type   | Description                                                              | Example                  |
| ------------------- | ------ | ------------------------------------------------------------------------ | ------------------------ |
| `LeaderID`          | String | A unique, URL-friendly identifier for the leader. **(Primary Key)**      | `putin_v`                |
| `FullName`          | String | The full name of the leader.                                             | `Vladimir Putin`         |
| `Country`           | String | The country the leader is associated with.                               | `Russia`                 |
| `DateAssumedPower`  | Date   | The "zero point" date in `YYYY-MM-DD` format.                            | `1999-12-31`             |
| `DateFellFromPower` | Date   | Optional: The date the leader left power (YYYY-MM-DD).                   | `null`                   |
| `BioSummary`        | String | A brief, one-paragraph biography.                                        | `Former KGB officer...`  |
| `Color`             | String | A hex color code for the leader's timeline ribbon.                       | `#DE3163`                |

### `Events` Sheet

This sheet contains all timeline events for all leaders.

| Column Name      | Type   | Description                                                              | Example                    |
| ---------------- | ------ | ------------------------------------------------------------------------ | -------------------------- |
| `EventID`        | String | A unique identifier for the event.                                       | `putin_event_001`          |
| `LeaderID`       | String | Links the event to a leader in the `Leaders` sheet. **(Foreign Key)**    | `putin_v`                  |
| `EventDate`      | Date   | The date the event occurred in `YYYY-MM-DD` format.                      | `2000-03-26`               |
| `EventType`      | String | A category for the event. Suggested: `Power`, `Economy`, `Military`, `Social`, `Foreign Policy`, `Opposition`. | `Power`                    |
| `EventTitle`     | String | A short, descriptive title for the event.                                | `First Presidential Election` |
| `EventDescription` | Text   | A longer description of the event and its significance.                  | `Won the election with...` |

---

## Local Development Setup

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

- Python 3.9+
- A Google Cloud Platform (GCP) project

### 2. Google API Setup

1.  Go to the Google Cloud Console.
2.  Create a new project.
3.  Enable the **Google Sheets API** and **Google Drive API**.
4.  Create a **Service Account**:
   - Go to `IAM & Admin` > `Service Accounts`.
   - Click `Create Service Account`.
   - Give it a name (e.g., `timeline-sheet-reader`).
   - Grant it the `Editor` role for basic read access.
   - Click `Done`. You will be returned to the list of service accounts.
   - Find the account you just created in the list and **click on its email address** to open its details page.
   - At the top of the service account details page, click on the **`KEYS`** tab.
   - Click `Add Key` > `Create new key`, and select **JSON**. A credentials file will be downloaded.
5.  **Secure Your Credentials**:
   - **DO NOT COMMIT THIS JSON FILE TO GIT.**
   - For local development, you can place it in the project root, but ensure your `.gitignore` file lists it.
6.  **Share the Google Sheet**:
   - Open the service account's JSON file and find the `client_email` address.
   - In your Google Sheet, click `Share` and add this email address, giving it "Editor" access.

### 3. Project Installation

```bash
# 1. Clone the repository
git clone https://github.com/stevewil/authoritarian-timeline.git
cd authoritarian-timeline

# 2. Create and activate a Python virtual environment
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Copy the example .env file
cp .env.example .env

# Now, edit the .env file with your specific credentials:
# Create a .env file in the root directory for local development
# (ensure .env is in your .gitignore)
# Add the following lines to the .env file:
```

### 4. Running the Backend Server

The FastAPI application is located in `api/main.py`. Run it with Uvicorn:

```bash
# This command tells uvicorn to run the 'app' object from the 'api.main' module
# --reload will automatically restart the server when you make code changes
uvicorn api.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You can view the automatic interactive documentation at `http://127.0.0.1:8000/docs`.

---

## Backend API

The backend exposes a single primary endpoint.

### `GET /api/timelines`

- **Description**: Fetches and returns all processed leader and event data.
- **Success Response (200 OK)**: Returns a JSON array where each object represents a leader and their timeline. The backend calculates `days_from_start` for each event relative to the leader's `DateAssumedPower`.

```json
[
  {
    "details": {
      "LeaderID": "putin_v",
      "FullName": "Vladimir Putin",
      "Country": "Russia",
      "DateAssumedPower": "1999-12-31",
      "Color": "#DE3163"
    },
    "events": [
      {
        "EventDate": "2000-03-26",
        "EventTitle": "First Presidential Election",
        "days_from_start": 86
      },
      { "...more events" }
    ]
  },
  { "...more leaders" }
]
```

---

## Frontend

The frontend is located in the `/public` directory. It should be a single-page application that:
1.  On load, makes a `fetch` request to the `/api/timelines` endpoint.
2.  Parses the JSON response.
3.  Uses a visualization library (like Vis.js) to render the data. Each leader becomes a "group" or "ribbon," and their events are placed as items on that ribbon according to the `days_from_start` value.
4.  Implements interactivity, such as tooltips on hover to show event details.

---

## Deployment

This project is configured for continuous deployment on Netlify.

- **Source**: The Netlify site is linked to the main branch of the GitHub repository.
- **Build Process**: The `netlify.toml` file configures the build. It tells Netlify:
  - How to install Python dependencies (`pip install -r requirements.txt`).
  - That the Python API in the `api/` directory should be treated as a serverless function.
  - That the `public/` directory contains the static frontend assets.
- **Environment Variables**: The Google Service Account credentials must be stored as a secure environment variable in the Netlify UI, not in the repository. The backend code will be configured to read these credentials from the environment when deployed.

Any push to the `main` branch will automatically trigger a new build and deployment on Netlify.
