from Invokes import invoke_http
import pika
import json
import pytz 
from datetime import datetime, timedelta, timezone
from threading import Thread

########################################## Flask Initalization Below ##########################################
from flask import Flask, request, jsonify
app = Flask(__name__)
########################################## Flask Initalization Above ##########################################

########################################## Calender Initalization Below ##########################################
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = '434c3a6f1d477740be91e0f73d98da3dfbcbef70d299c5a53c542d3e40e29de5@group.calendar.google.com'
TIMEOFFSET = '+08:00'

calender_cred = service_account.Credentials.from_service_account_file("backend/config/calender_credential.json", scopes = SCOPES)
calendar = build('calendar', 'v3', credentials = calender_cred)
########################################## Calender Initalization Above ##########################################

########################################## Calender Helper Below ##########################################
# Deletes all lessons from student's telegram     
def delete_all_stu_lessons(telegram):
    
    page_token = None
    while True:
        events = calendar.events().list(calendarId=CALENDAR_ID, pageToken=page_token).execute()
        for event in events['items']:
            # Check if the event's extended properties match the student's Telegram 
            if 'extendedProperties' in event and 'private' in event['extendedProperties'] and 'telegram' in event['extendedProperties']['private']:
                if event['extendedProperties']['private']['telegram'] == telegram:
                    # Delete the event
                    try:
                        calendar.events().delete(calendarId=CALENDAR_ID, eventId=event['id']).execute()
                        print(f"Deleted event: {event['summary']} for @{telegram}")
                    except Exception as e:
                        print(f"Failed to delete event: {event['summary']} for @{telegram}. Error: {e}")
        
        page_token = events.get('nextPageToken')
        if not page_token:
            break

def find_week_of_event(service, calendar_id, selected_lesson_eventID):
    """Find the date of the event."""
    try:
        event = service.events().get(calendarId=calendar_id, eventId=selected_lesson_eventID).execute()
        start_date = event['start'].get('date') or event['start'].get('dateTime')
        start_date = datetime.fromisoformat(start_date)
        return start_date
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def get_week_range_from_date(date):
    """Given a date, return the start and end of its week (Monday to Sunday)."""
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)
    return start, end        

# def find_available_timeslots_week(calendar_service, calendar_id, start, end):
#     """Find available timeslots within a specified week, excluding busy days and past dates."""
#     timezone_str = 'Asia/Singapore'  # Adjust according to your needs
#     timezone = pytz.timezone(timezone_str)
    
#     # Ensure start and end are datetime objects for calculation
#     start_dt = datetime.combine(start, datetime.min.time()).replace(tzinfo=timezone)
#     end_dt = datetime.combine(end, datetime.max.time()).replace(tzinfo=timezone)
    
#     # Get the current time in the specified timezone to compare with slots
#     now = datetime.now(timezone)
    
#     # Convert to string only for the API call
#     time_min = start_dt.isoformat()
#     time_max = end_dt.isoformat()

#     try:
#         events_result = calendar_service.events().list(
#             calendarId=calendar_id, 
#             timeMin=time_min, 
#             timeMax=time_max, 
#             singleEvents = True,
#             orderBy='startTime'
#         ).execute()
#         events = events_result.get('items', [])

#         available_slots_list = []
#         for single_date in (start_dt + timedelta(days=n) for n in range((end_dt - start_dt).days + 1)):
#             if single_date.weekday() not in [1, 3, 5]:  # Excluding specific weekdays
#                 for hour in range(10, 18):  # Assuming availability from 10am to 6pm
#                     # Combine date and hour into a single datetime object
#                     slot_datetime = datetime.combine(single_date.date(), datetime.min.time()).replace(hour=hour, tzinfo=timezone)
#                     # Skip slots that are in the past
#                     if slot_datetime < now:
#                         continue
#                     # Format the datetime object to the ISO 8601 string with timezone
#                     slot_iso = slot_datetime.isoformat()
#                     available_slots_list.append(slot_iso)

#         return available_slots_list
#     except Exception as e:
#         print(f"Error finding available timeslots: {e}")
#         return []

def find_available_timeslots_week(calendar_service, calendar_id, start, end):
    """Find available timeslots within a specified week, excluding busy days, past dates, and times when events are already scheduled."""
    timezone_str = 'Asia/Singapore'  # Adjust according to your needs
    timezone = pytz.timezone(timezone_str)
    
    # Ensure start and end are datetime objects for calculation
    start_dt = datetime.combine(start, datetime.min.time()).replace(tzinfo=timezone)
    end_dt = datetime.combine(end, datetime.max.time()).replace(tzinfo=timezone)
    
    # Get the current time in the specified timezone to compare with slots
    now = datetime.now(timezone)
    
    # Convert to string only for the API call
    time_min = start_dt.isoformat()
    time_max = end_dt.isoformat()

    try:
        events_result = calendar_service.events().list(
            calendarId=calendar_id, 
            timeMin=time_min, 
            timeMax=time_max, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        # Collect start and end times of existing events to check against potential slots
        event_times = [(datetime.fromisoformat(event['start'].get('dateTime') or event['start'].get('date')).replace(tzinfo=timezone),
                        datetime.fromisoformat(event['end'].get('dateTime') or event['end'].get('date')).replace(tzinfo=timezone))
                       for event in events]

        available_slots_list = []
        for single_date in (start_dt + timedelta(days=n) for n in range((end_dt - start_dt).days + 1)):
            if single_date.weekday() not in [1, 3, 5]:  # Adjusting excluded weekdays
                for hour in range(10, 18):  # Assuming availability from 10am to 6pm
                    # Combine date and hour into a single datetime object for the slot start time
                    potential_slot_start = datetime.combine(single_date.date(), datetime.min.time()).replace(hour=hour, tzinfo=timezone)
                    potential_slot_end = potential_slot_start + timedelta(hours=1)  # Assuming 1-hour slots for simplicity
                    
                    # Check if the potential slot overlaps with any scheduled events
                    if any(event_start <= potential_slot_start < event_end or event_start < potential_slot_end <= event_end for event_start, event_end in event_times):
                        continue  # Skip this slot as it overlaps with an existing event
                    
                    # Skip slots that are in the past
                    if potential_slot_start < now:
                        continue
                    
                    # Format the datetime object to the ISO 8601 string with timezone
                    slot_iso = potential_slot_start.isoformat()
                    available_slots_list.append(slot_iso)

        return available_slots_list
    except Exception as e:
        print(f"Error finding available timeslots: {e}")
        return []


    
def delete_by_eventID(eventID):
    try:
        # Attempt to delete the event
        calendar.events().delete(calendarId=CALENDAR_ID, eventId=eventID).execute()
        print(f"Successfully deleted event: {eventID}")
    except Exception as e:
        print(f"Error deleting event {eventID}: {e}")

def create_event(name, telegram, lesson_start, lesson_end):
    event = {
        'summary': f'Coding Lesson: {name}',
        'description': f'Tele Handle: @{telegram}',
        'start': {
            'dateTime': lesson_start,
            'timeZone': 'Asia/Singapore',
        },
        'end': {
            'dateTime': lesson_end,
            'timeZone': 'Asia/Singapore',
        },
        'extendedProperties': {
            'private': {
                'telegram': telegram,  # Store Telegram handle for easy retrieval
            }
        }
    }

    try:
        # Insert the event into Google Calendar
        response = calendar.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        print(f"Event created: {response.get('htmlLink')}")
    except Exception as e:
        print(f"Error creating calendar event for {name}: {e}")

########################################## Calender Helper Above ##########################################

########################################## Populating Calender Below ##########################################
def listen_onboarding():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='onboarding')

    channel.basic_consume(queue="onboarding", on_message_callback=parse_onboarding_data, auto_ack=False)

    channel.start_consuming()

def parse_onboarding_data(ch, method, properties, body):
    student_data = json.loads(body)
    print("Received Stu Data", student_data)
    try:
        # Extracting necessary information from student_data
        first_lesson_start, lesson_duration_hours, num_of_lessons = student_data["schedule"]
        
        # Convert lesson duration and number of lessons to integers
        lesson_duration_hours = int(lesson_duration_hours)
        num_of_lessons = int(num_of_lessons)
            
        # Calculate the end time based on the start time and lesson duration
        end_time = (datetime.fromisoformat(first_lesson_start[:-6]) + timedelta(hours=lesson_duration_hours)).isoformat() + first_lesson_start[-6:]

        # Call populate_calendar with extracted data and end time
        populate_calendar(
            name=student_data["name"],
            telegram=student_data["telegram"],
            lesson_start=first_lesson_start,
            lesson_end=end_time,
            num_lessons=num_of_lessons
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("Error: Failed to process message", str(e))


# def populate_calendar(name, telegram, lesson_start, lesson_end, num_lessons):
#     # Prepare the recurrence rule based on the number of lessons
#     recurrence_rule = f"RRULE:FREQ=WEEKLY;COUNT={num_lessons}"

#     event = {
#         'summary': f'Coding Lesson: {name}',
#         'description': f'Tele Handle: @{telegram}',
#         'start': {
#             'dateTime': lesson_start,
#             'timeZone': 'Asia/Singapore',
#         },
#         'end': {
#             'dateTime': lesson_end,
#             'timeZone': 'Asia/Singapore',
#         },
#         'recurrence': [recurrence_rule],
#         'extendedProperties': {
#             'private': {
#                 'telegram': telegram,  # Store Telegram handle for easy retrieval & We should also find a way to store stuID so that we can ensure there will be no issue!
#             }
#         }
#     }

#     try:
#         # Insert the event into Google Calendar
#         response = calendar.events().insert(calendarId=CALENDAR_ID, body=event).execute()
#         print(f"Event created: {response.get('htmlLink')}")
#     except Exception as e:
#         print(f"Error creating calendar event: {e}")
def populate_calendar(name, telegram, lesson_start, lesson_end, num_lessons):
    # Convert the start and end times to datetime objects
    start_dt = datetime.fromisoformat(lesson_start)
    end_dt = datetime.fromisoformat(lesson_end)
    
    # Loop through the number of lessons to create an event for each lesson
    for lesson_num in range(num_lessons):
        event = {
            'summary': f'Coding Lesson: {name}',
            'description': f'Tele Handle: @{telegram}',
            'start': {
                'dateTime': start_dt.isoformat(),
                'timeZone': 'Asia/Singapore',
            },
            'end': {
                'dateTime': end_dt.isoformat(),
                'timeZone': 'Asia/Singapore',
            },
            'extendedProperties': {
                'private': {
                    'telegram': telegram,  # Store Telegram handle for easy retrieval
                }
            }
        }
        
        try:
            # Insert the event into Google Calendar
            response = calendar.events().insert(calendarId=CALENDAR_ID, body=event).execute()
            print(f"Event created: {response.get('htmlLink')}")
        except Exception as e:
            print(f"Error creating calendar event for {name}: {e}")
        
        # Update start and end datetimes for the next lesson, assuming a weekly interval
        start_dt += timedelta(weeks=1)
        end_dt += timedelta(weeks=1)

########################################## Populating Calender Above ##########################################
        
########################################## Upcoming Reschedule Calender Below ##########################################
        
@app.route("/schedule/fetch_upcoming_lessons", methods=['POST'])
def fetch_upcoming_lessons():
    data = request.get_json()
    telegram_username = data.get("telegram_username")  # Extract telegram from POST request data

    singapore_timezone = pytz.timezone('Asia/Singapore')
    time_min = datetime.now(singapore_timezone) + timedelta(days=1)
    time_min = time_min.isoformat()

    upcoming_lessons = []  # Initialize as a dictionary

    try:
        events_result = calendar.events().list(
            calendarId=CALENDAR_ID,
            timeMin=time_min,
            maxResults=4,  # Limit to the next 4 upcoming lessons
            singleEvents=True,
            orderBy='startTime',
            privateExtendedProperty=f"telegram={telegram_username}"
        ).execute()
        
        events = events_result.get('items', [])

        for event in events:
            event_id = event['id']  # Get event ID
            event_start = event['start'].get('dateTime', event['start'].get('date'))
            upcoming_lessons.append([event_id,event_start])
            # upcoming_lessons[event_id] = event_start  # Correctly add to dictionary
        print(upcoming_lessons)
        return jsonify({"upcoming_lessons": upcoming_lessons})

    except Exception as e:
        print(f"Failed to fetch upcoming lessons: {str(e)}")
        return jsonify({"error": "Failed to fetch upcoming lessons"}), 500
    
@app.route('/schedule/find_available_slots_week', methods=['POST'])
def find_available_slots_week():
    data = request.get_json()
    selected_lesson_eventID = data.get("selected_lesson_eventID")

    if not selected_lesson_eventID:
        return jsonify({"error": "Event ID is required"}), 400

    try:
        # Find the date of the event using the provided event ID
        event_date = find_week_of_event(calendar, CALENDAR_ID, selected_lesson_eventID)
        if not event_date:
            return jsonify({"error": "Event not found"}), 404
        
        # Determine the start and end of the week for the event's date
        start_of_week, end_of_week = get_week_range_from_date(event_date)
        
        available_timeslots_week = find_available_timeslots_week(calendar, CALENDAR_ID, start_of_week, end_of_week)
        
        return jsonify({"available_timeslots_week": available_timeslots_week})
    
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "Failed to process request"}), 500

def listen_rescheduling():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='rescheduling')

    channel.basic_consume(queue="rescheduling", on_message_callback=parse_rescheduling_data, auto_ack=False)

    channel.start_consuming()

def parse_rescheduling_data(ch, method, properties, body):
    reschedule_data = json.loads(body)
    print("Received Rescheduling Data", reschedule_data)
    
    try:
        eventID, new_lesson_str, username = reschedule_data["rescheduling"]
        
        # Fetch the old event to get its start time and ensure we're using the correct year
        old_event = calendar.events().get(calendarId=CALENDAR_ID, eventId=eventID).execute()
        old_event_year = datetime.fromisoformat(old_event['start']['dateTime']).year

        # Adjust the new lesson string to use the correct year and ensure correct timezone from the start
        new_lesson_datetime = datetime.strptime(new_lesson_str, "%d %b, %H:%M").replace(year=old_event_year)
        timezone = pytz.timezone('Asia/Singapore')
        start_time = timezone.localize(new_lesson_datetime)

        # Extract student name from the old event summary
        stu_name = old_event['summary'].replace('Coding Lesson: ', '')

        # Calculate duration and new end time
        old_start = datetime.fromisoformat(old_event['start']['dateTime'])
        old_end = datetime.fromisoformat(old_event['end']['dateTime'])
        duration = old_end - old_start
        
        # Calculate new end time based on duration and ensure it has the correct timezone
        new_end_time = start_time + duration
        # Note: No need to localize new_end_time if start_time is already localized

        # Proceed with updating the calendar
        update_reschedule(eventID, stu_name, username, start_time.isoformat(), new_end_time.isoformat())

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error: Failed to process message due to {e}")

def update_reschedule(eventID, name, telegram, lesson_start, lesson_end):
    delete_by_eventID(eventID)  # Assumes this function deletes the event by ID
    create_event(name, telegram, lesson_start, lesson_end)  # Adjusted version of populate_calendar without recurrence

########################################## Upcoming Reschedule Calender Above ##########################################

@app.route('/schedule/get_recent_events', methods=['GET'])
def get_events_last_day():
    singapore_timezone = pytz.timezone('Asia/Singapore')
    now = datetime.now(singapore_timezone)
    one_day_ago = now - timedelta(days=1)

    time_min = one_day_ago.isoformat()
    time_max = now.isoformat()

    try:
        events_result = calendar.events().list(
            calendarId=CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        # Process the events as needed for your application
        processed_events = []
        for event in events:
            # Example: Extract and format event data
            event_data = {
                'id': event['id'],
                'summary': event.get('summary', 'No Title'),
                'start': event['start'].get('dateTime', event['start'].get('date')),
                'end': event['end'].get('dateTime', event['end'].get('date')),
                'telegram': event['extendedProperties']['private'].get('telegram', 'No Telegram Username'),
            }
            processed_events.append(event_data)

        return jsonify({"recent_events": processed_events}), 200
        # return jsonify( processed_events), 200


    except Exception as e:
        print(f"Failed to fetch events: {str(e)}")
        return jsonify({"error": "Failed to fetch events"}), 500
       
def start_rabbitmq_listener():
    print("one running")
    thread1 = Thread(target=listen_onboarding)
    thread1.start()

    thread2 = Thread(target=listen_rescheduling)
    thread2.start()

if __name__ == '__main__':
    # Start RabbitMQ listener in a separate thread
    rabbitmq_thread = Thread(target=start_rabbitmq_listener)
    rabbitmq_thread.start()

    # Start Flask app in the main thread
    app.run(debug=True, port=5002)