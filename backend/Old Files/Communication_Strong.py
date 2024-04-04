from flask import Flask, request, jsonify

app = Flask(__name__)
########################################## Data Fetching Functions Below ##########################################
def fetch_upcoming_lessons(username):
    return ['1 April', '8 April', '15 April', '22 April']

def fetch_available_timeslots_all():
    return ['Monday 1800', 'Wednesday 1800', 'Saturday 1800']

def fetch_available_timeslot_week(date):
    return ['Tuesday 1800', 'Thursday 1800']
########################################## Data Fetching Functions Above ##########################################

### Dispatcher Below
dispatcher = {
    "fetch_upcoming_lessons": {
        "function": fetch_upcoming_lessons,
        "params": ["username"]
    },
    "fetch_available_timeslots_all": {
        "function": fetch_available_timeslots_all
    },
    "fetch_available_timeslot_week": {
        "function": fetch_available_timeslot_week,
        "params": ["date"]
    }
}
### Dispatcher Above

@app.route("/")
def home():
    return "Home Page!"

# Routes and dispatches to appropriate functions
@app.route('/process_message', methods=['POST'])
def process_message():
    payload = request.get_json()

    #username = payload.get("username")
    action = payload.get("request")

    # Handles Error: Unrecognized Request
    if action not in dispatcher:
        return jsonify({"error": "Request not recognized"}), 400
    
    # What Func to Call
    func = dispatcher[action]["function"]
    # What Params Needed
    params =  dispatcher[action].get("params", [])
    # Collect params from payload
    args = {param: payload.get(param) for param in params if param in payload}
    # Handles Error: Missing Params
    if len(args) < len(params):
        missing_params = set(params) - set(args.keys())
        return jsonify({"error": "Missing required parameters", "missing": list(missing_params)}), 400
   
    return jsonify({"data": func(**args)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)