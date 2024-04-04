from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask import Flask, request, jsonify
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("./service_acc.json")
firebase_admin.initialize_app(cred)
db = firestore.client() 
app = Flask(__name__)

# Google calendar API settings
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_PATH = '/credential.json'
CALENDAR_ID = '434c3a6f1d477740be91e0f73d98da3dfbcbef70d299c5a53c542d3e40e29de5@group.calendar.google.com'
TIMEOFFSET = '+08:00'

# Initialize Google Calendar
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
calendar = build('calendar', 'v3', credentials=credentials)


# Function to insert new event to Google Calendar
def insert_event(event):
    try:
        response = calendar.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        if response.get('status') == 'confirmed':
            return 1
        else:
            return 0
    except Exception as e:
        print(f"Error:  insert_event --> {e}")
        return 0


@app.route("/google_calendar", methods=['POST'])
def create_schedule():
    try:
        # Extract event details from the JSON sent via Postman
        data = request.json
        if not data:
            return "No data provided", 400  # Bad Request if no data provided
        
        # Check if all required fields are present
        required_fields = ['summary', 'description', 'start_datetime', 'end_datetime']
        for field in required_fields:
            if field not in data:
                return f"Missing required field: {field}", 400
        
        # Construct the event dictionary
        event = {
            'summary': data['summary'],
            'description': data['description'],
            'start': {
                'dateTime': data['start_datetime'],
                'timeZone': 'Asia/Singapore'
            },
            'end': {
                'dateTime': data['end_datetime'],
                'timeZone': 'Asia/Singapore'
            }
        }

        # Add recurrence rule if provided
        if 'recurrence' in data:
            event['recurrence'] = [data['recurrence']]
        
        # Insert event into Google Calendar
        result = insert_event(event)
        
        if result == 1:
            # Add the event document to Firestore
            db.collection('tuition_schedule').add(event)
            return "Event created successfully"
        else:
            return "Failed to create event in Google Calendar"
    except Exception as e:
        print(f"Error at create_schedule --> {e}")
        return "Failed to create event"


def get_events(date_time_start, date_time_end):
    try:
        response = calendar.events().list(calendarId=CALENDAR_ID, timeMin=date_time_start, timeMax=date_time_end, timeZone='Asia/Singapore').execute()
        items = response.get('items', [])
        return items
    except Exception as e:
        print(f"Error at get_events --> {e}")
        return []



def add_events_to_firestore(events):
    try:
        for event in events:
            event_id = event['id']
            # Check if the document with the event_id already exists
            existing_doc = db.collection('timing').document(event_id).get()
            if existing_doc.exists:
                print(f"Event with ID {event_id} already exists, skipping...")
                continue  # Skip adding the event if it already exists
            # If the document doesn't exist, add the event to Firestore
            start_datetime = event['start']['dateTime']
            end_datetime = event['end']['dateTime']
            start_date, start_time = start_datetime.split('T')
            end_date, end_time = end_datetime.split('T')
            summary = event['summary']
            db.collection('timing').document(event_id).set({
                'start_date': start_date,
                'start_time': start_time,
                'end_date': end_date,
                'end_time': end_time,
                'event_id': event_id,
                'summary': summary,
            })
        return True
    except Exception as e:
        print(f"Error at add_events_to_firestore --> {e}")
        return False
# Define your Flask route



@app.route("/google_calendar", methods=['GET'])
def get_event():
    try:
        # Extract start_date and end_date from the query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Ensure start_date and end_date are provided
        if not start_date or not end_date:
            return "Please provide both start_date and end_date as query parameters", 400

        # Call the function to get events based on the provided dates
        events = get_events(start_date, end_date)
        # return events 
        success = add_events_to_firestore(events)

        if success:
            return "Events added to Firestore successfully", 200
        else:
            return "Failed to add events to Firestore", 500

        
    except Exception as e:
        print(f"Error at get_event --> {e}")
        return "Failed to get event", 500












def delete_event(event_id):
    try:
        calendar.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
        return 1
    except Exception as e:
        print(f"Error at delete_event --> {e}")
        return 0






@app.route("/google_calendar", methods=['DELETE'])
def delete_event_route():
    try:
        # Extract event_id from the query parameters
        event_id = request.args.get('event_id')
        if not event_id:
            return "Event ID not provided in the query parameters", 400
        
        # Delete event from Firestore
        event_ref = db.collection('timing').document(event_id)
        event_data = event_ref.get()
        if event_data.exists:
            event_ref.delete()
        else:
            return "Event not found in Firestore", 404
    except Exception as e:
        print(f"Error at delete_event_route (Firestore) --> {e}")
        return "Failed to delete event from Firestore", 500

    try:
        # Delete event from Google Calendar
        result = delete_event(event_id)
        if result == 1:
            return "Event deleted successfully"
        else:
            return "Failed to delete event from Google Calendar", 500
    except Exception as e:
        print(f"Error at delete_event_route (Google Calendar) --> {e}")
        return "Failed to delete event from Google Calendar", 500

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port=5000, debug=True)

