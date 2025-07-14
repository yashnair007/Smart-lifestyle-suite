import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import requests
from datetime import datetime, timedelta, timezone
import pandas as pd
import pytz

# Define activity types mapping
activity_types = {
    0: "In vehicle", 1: "Biking", 2: "On foot", 3: "Still", 4: "Unknown", 5: "Tilting", 7: "Walking",
    8: "Running", 9: "Aerobics", 10: "Badminton", 14: "Handbiking", 72: "REM sleep", 83: "Still",
    96: "Moving", 69: "Sleeping", 70: "Light sleep", 71: "Deep sleep", 100: "Zumba"
}

# Define timezone (UTC to match your data, can switch to IST if needed)
IST = pytz.timezone('Asia/Kolkata')

def fmt(ms):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')

def init_fit_service():
    creds_file = "client_secret.json"
    creds_path = os.path.join(os.path.dirname(__file__), creds_file)
    if not os.path.exists(creds_path):
        raise FileNotFoundError("client_secret.json not found. Please set up Google Fit API credentials.")

    # Token storage
    creds = None
    token_path = "token.pickle"
    scopes = [
        "https://www.googleapis.com/auth/fitness.activity.read",
        "https://www.googleapis.com/auth/fitness.location.read",
        "https://www.googleapis.com/auth/fitness.body.read",
        "https://www.googleapis.com/auth/fitness.sleep.read"
    ]

    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            creds_path, scopes
        )
        creds = flow.run_local_server(port=0)
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return build("fitness", "v1", credentials=creds, cache_discovery=False)

def get_fit_sessions(service, start_hours_ago=24):
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=start_hours_ago)
    start_rfc = start.isoformat()
    end_rfc = now.isoformat()

    sessions = service.users().sessions().list(
        userId="me",
        startTime=start_rfc,
        endTime=end_rfc
    ).execute().get("session", [])

    if not sessions:
        return pd.DataFrame()

    data = []
    for sess in sessions:
        name = sess.get('name', 'Unnamed')
        atype_code = sess.get('activityType', 4)
        atype = activity_types.get(atype_code, f"Activity Type {atype_code}")
        start_ms = int(sess['startTimeMillis'])
        end_ms = int(sess['endTimeMillis'])
        duration = (end_ms - start_ms) / (1000 * 60)  # Convert to minutes

        # Aggregate Metrics
        metrics = {
            'com.google.step_count.delta': "Steps",
            'com.google.distance.delta': "Distance (m)",
            'com.google.calories.expended': "Calories"
        }

        req = {
            "aggregateBy": [{"dataTypeName": k} for k in metrics],
            "bucketByTime": {"durationMillis": end_ms - start_ms},
            "startTimeMillis": start_ms,
            "endTimeMillis": end_ms
        }

        try:
            agg = service.users().dataset().aggregate(userId="me", body=req).execute()
            found = {k: None for k in metrics}

            for b in agg.get("bucket", []):
                for ds in b.get("dataset", []):
                    dt = ds.get("dataSourceId", "")
                    for pt in ds.get("point", []):
                        dtype = pt.get("dataTypeName", "")
                        val = pt.get("value", [{}])[0]
                        num = val.get("fpVal") or val.get("intVal")
                        if dtype in metrics:
                            found[dtype] = num

            row = {
                "date": fmt(start_ms),
                "type": atype,
                "name": name,
                "duration_minutes": round(duration, 2),
                "steps": found['com.google.step_count.delta'],
                "distance_m": found['com.google.distance.delta'],
                "calories": found['com.google.calories.expended']
            }
            # Only set sleep duration, no calories
            if atype.lower() in ["rem sleep", "light sleep", "deep sleep", "sleeping"]:
                row["steps"] = 0
                row["distance_m"] = 0
                row["calories"] = None  # Remove calorie estimate
            data.append(row)
        except Exception as e:
            print(f"⚠️ Error retrieving metrics for {name}: {e}")
            row = {
                "date": fmt(start_ms),
                "type": atype,
                "name": name,
                "duration_minutes": round(duration, 2),
                "steps": 0,
                "distance_m": 0,
                "calories": 0
            }
            if atype.lower() in ["rem sleep", "light sleep", "deep sleep", "sleeping"]:
                row["calories"] = None  # No calories for sleep
            data.append(row)

    return pd.DataFrame(data)

def log_fit_to_exercise(exercise_log_file, fit_data=None):
    if fit_data is None:
        service = init_fit_service()
        fit_data = get_fit_sessions(service)
    if fit_data.empty:
        return False

    if os.path.exists(exercise_log_file):
        exercise_log = pd.read_csv(exercise_log_file)
    else:
        exercise_log = pd.DataFrame(columns=["date", "type", "duration", "intensity", "est_calories", "heart_rate", "steps", "notes"])

    for _, row in fit_data.iterrows():
        date = row["date"]
        atype = row["type"]
        if not exercise_log[(exercise_log["date"] == date) & (exercise_log["type"] == atype)].empty:
            continue
        new_entry = pd.DataFrame([{
            "date": date,
            "type": atype,
            "duration": row["duration_minutes"],
            "intensity": "auto",
            "est_calories": row["calories"] if row["calories"] is not None else 0,
            "heart_rate": 0,
            "steps": row["steps"] or 0,
            "notes": f"Imported from Google Fit: {row['name']}"
        }])
        exercise_log = pd.concat([exercise_log, new_entry], ignore_index=True)

    exercise_log.to_csv(exercise_log_file, index=False)
    return True