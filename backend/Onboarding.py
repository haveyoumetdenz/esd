from Invokes import invoke_http
import pika
import json

########################################## Flask Initalization Below ##########################################
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
########################################## Flask Initalization Above ##########################################

########################################## Firebase Initalization Below ##########################################
import firebase_admin
from firebase_admin import credentials, firestore

firestore_cred = credentials.Certificate('backend/config/onboarding_db_credential.json')  
firebase_admin.initialize_app(firestore_cred)
db = firestore.client()
########################################## Firebase Initalization Above ##########################################

# test_student = {
#     "name": "Ryan Khoo",
#     "telegram": "ryankzl",
#     "poc": [poc name, poc tele]"seekenn",
#     "age": 23,
#     "schedule": ["2024-04-08T15:00:00+08:00", 2, 10] # First Lesson, Lesson Duration, Num of Lessons
# }

# We will try to include this at the front end some way so as to prevent dual insertion?
def generate_student_id():
    @firestore.transactional
    def increment_and_format_id(transaction):
        counter_ref = db.collection('metadata').document('studentCounter')
        counter_snapshot = counter_ref.get(transaction=transaction)

        if counter_snapshot.exists:
            current_count = counter_snapshot.get('count')
        else:
            current_count = 0
        new_count = current_count + 1

        formatted_id = f"{new_count:04}"
        transaction.set(counter_ref, {'count': new_count})

        return formatted_id

    transaction = db.transaction()
    return increment_and_format_id(transaction)

@app.route("/onboarding/onboard_student", methods=['POST'])
def onboard_student():
    try:
        student_data = request.json
        
        stuID = generate_student_id()

        db.collection("Students").document(stuID).set(student_data)
        
        publish_onboard_message(student_data)
       
        # Return a success response
        return jsonify({"success": True, "stuID": stuID}), 200
    except Exception as e:
         # Return an error response in case of failure
        return jsonify({"success": False, "error": str(e)}), 500

def publish_onboard_message(student_data):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue = "onboarding")
    print("publishing")
    channel.basic_publish(
        exchange="",
        routing_key="onboarding",
        body = json.dumps(student_data)
    )
    connection.close

if __name__ == '__main__':
    app.run(debug=True, port=5001)