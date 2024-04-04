import pika
import json
from threading import Thread
from Invokes import invoke_http
########################################## Flask Initalization Below ##########################################
from flask import Flask, request, jsonify
app = Flask(__name__)
########################################## Flask Initalization Above ##########################################

########################################## Firebase Initalization Below ##########################################
import firebase_admin
from firebase_admin import credentials, firestore

firestore_cred = credentials.Certificate('backend/config/progress_db_credential.json')  
firebase_admin.initialize_app(firestore_cred)
db = firestore.client()
########################################## Firebase Initalization Above ##########################################

@app.route('/progress', methods=['GET'])
def get_recent_events():
    url = "http://127.0.0.1:5002/schedule/get_recent_events"
    
    response = invoke_http(url, method="GET")
    
    if response.get("code", 200) == 200:
        events = response.get("recent_events", [])  # Assuming the response data is under 'data'
        
        # events will look like this:
        #     [
        # {
        #     "end": "2024-04-03T17:00:00+08:00",
        #     "id": "g3aore1pmjfgps3em9g7uf6b1o",
        #     "start": "2024-04-03T15:00:00+08:00",
        #     "summary": "Coding Lesson: Ryan Khoo"
        # }
        #]   
        return jsonify(events), 200

    else:
        error_message = response.get("message", "Unknown error occurred.")
        print("Error: get_recent_events", error_message)
        return jsonify({"error": error_message}), 500


@app.route("/progress/update_student_progress", methods=["POST"])
def update_student_progress():
    try:
        progress_report = request.json
        stuID = progress_report["stuID"]
        eventID = progress_report["eventID"]
        report_content = progress_report["report"]

        # Prepare the report data where eventID is the key, and report_content is the value
        report_data = {eventID: report_content}

        # Update the document for the student with the new report
        # This will add the new eventID-report pair or overwrite the report for an existing eventID
        db.collection("Progress Reports").document(stuID).set(report_data, merge=True)
       
        return jsonify({"success": True, "stuID": stuID, "eventID": eventID}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
########################################## DB Population Below ##########################################

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
        # Extract Key Deets
        poc_telegram = student_data["poc"][1]
        student_name = student_data["name"]
        student_telegram = student_data["telegram"]

        populate_poc_child_database(poc_telegram,student_name,student_telegram)

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("Error: Failed to process message", str(e))

def populate_poc_child_database(poc_telegram, student_name, student_telegram):
        
    try:
        document_data = {
        "student_name": student_name,
        "student_telegram": student_telegram
        }
    
        db.collection("poc_student").document(poc_telegram).set(document_data)
       
        # Return a success response
        print("Succesful Creation of POC-Child")
    except Exception as e:
         # Return an error response in case of failure
        print("Error in Creation of POC-Child")


########################################## DB Population Above ##########################################

def start_rabbitmq_listener():
    thread = Thread(target=listen_onboarding)
    thread.start()

if __name__ == '__main__':
    # Start RabbitMQ listener in a separate thread
    rabbitmq_thread = Thread(target=start_rabbitmq_listener)
    rabbitmq_thread.start()

    # Start Flask app in the main thread
    app.run(debug=True, port=5005)