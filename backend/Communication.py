from Invokes import invoke_http
from datetime import datetime 
from threading import Thread
import pytz
import pika
import json
########################################## Flask Initalization Below ##########################################
from flask import Flask, request, jsonify
app = Flask(__name__)
########################################## Flask Initalization Above ##########################################

@app.route("/communication/prepare_upcoming_lessons", methods = ['POST'])
def prepare_upcoming_lessons():
    # This is from telegram
    payload = request.get_json()
    telegram_username = payload.get("telegram_username")

    # THis is sending to calender
    url = "http://127.0.0.1:5001/schedule/fetch_upcoming_lessons"
    payload = {
        "telegram_username": telegram_username,
    }

    response = invoke_http(url, method = "POST", json = payload)

    if response.get("code", 200) == 200:
        upcoming_lessons = response.get("upcoming_lessons", {})
        print(upcoming_lessons)
        upcoming_lessons_formatted = []
       
        # for event_id, event_time in upcoming_lessons.items():
        for event in upcoming_lessons:
            event_datetime = datetime.fromisoformat(event[1])
            # event_datetime = datetime.fromisoformat(event_time)
            date_time_formatted = event_datetime.strftime('%d %b, %H:%M')
            
            # Format the output message
            upcoming_lessons_formatted.append([date_time_formatted, event[0]])
        # print(upcoming_lessons_formatted)
        return jsonify({"upcoming_lessons_formatted": upcoming_lessons_formatted})
    
    else:
        return "Error: upcoming_lessons", response.get("message")

@app.route("/communication/get_weekly_available_timeslots", methods=["POST"])
def get_weekly_available_timeslots():
    payload = request.get_json()
    selected_lesson_eventID = payload.get("selected_lesson_eventID")

    if not selected_lesson_eventID:
        return jsonify({"error": "Event ID is required"}), 400

    # This is sending to calendar
    url = "http://127.0.0.1:5001/schedule/find_available_slots_week"
    response = invoke_http(url, method="POST", json={"selected_lesson_eventID": selected_lesson_eventID})

    if response.get("code",200) == 200:

        available_slots_list = response.get("available_timeslots_week", [])
        print(available_slots_list)
        available_timeslots_week_formatted = []
        
        for slot in available_slots_list:
            slot_datetime = datetime.fromisoformat(slot)
            slot_datetime_formatted = slot_datetime.strftime('%d %b, %H:%M')
            available_timeslots_week_formatted.append(slot_datetime_formatted)

        return jsonify({"available_timeslots_week_formatted": available_timeslots_week_formatted})
    else:
        return jsonify({"error": response.get("message", "Failed to fetch available slots")}), 500

# Rabbit for this
@app.route("/communication/update_reschedule", methods = ["POST"])
def update_reschedule():
    payload = request.get_json()
    username = payload.get("username")
    eventID = payload.get("eventID")
    new_lesson = payload.get("new_lesson")
    reschedule_data = [eventID,new_lesson,username]
    message = {"rescheduling": reschedule_data}
    publish_reschedule_message(message)

    return jsonify({"success": True}), 200

def publish_reschedule_message(reschedule_data):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost")
    )
    channel = connection.channel()
    channel.queue_declare(queue = "rescheduling")

    channel.basic_publish(
        exchange="",
        routing_key="rescheduling",
        body = json.dumps(reschedule_data)
    )
    connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)