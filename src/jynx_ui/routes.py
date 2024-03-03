from jynx_ui.application import app
from flask import render_template, request, jsonify, send_from_directory
import os
import json
import requests

app_root = os.path.dirname(os.path.abspath(__file__))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app_root, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template('index.html')


def bot_response(message):
    json_out = {}
    url = "http://localhost:5885/submit"
    data = {
        'user_input': message
    }
    try:
        response = requests.post(url, data=data)
        resp = json.loads(response.text)
        print(resp)
        status = resp.get("status", False)
        json_out = {
                       "status": status,
                       "message": resp.get("name", "warning - no task run.")
                   }
        return json_out
    except Exception as e:
        print("Error:", e)
        json_out = {
                       "status": False,
                       "message": resp.get("name", "error - no task run.")
                   }
        return json_out
    return json_out


@app.route('/submit_message', methods=['POST'])
def submit_message():
    json_out = {
        "status": False
    }
    message = request.json['message']
    chat_name = request.json['chat_name']
    # Process the message here
    # Store the conversation in JSON format
    chat_data = {}
    chat_file_path = os.path.join(app_root, "history", f"{chat_name}.json")
    with open(chat_file_path, "r") as f:
        chat_data = json.loads(f.read())
    if chat_data != {}:
        chat_data["chats"].append({"user": message})
        b_resp = bot_response(message)
        chat_data["chats"].append({"bot": f'Task Status: {b_resp["message"]}'})
        with open(chat_file_path, "w") as f:
            f.write(json.dumps(chat_data, indent=2))
        json_out.update({
            "status": b_resp["status"],
            "message": f'Task Status: {b_resp["message"]}'
        })

    return json_out


@app.route('/chat_list')
def chat_list():
    json_chat_list = {}
    the_path = os.path.join(app_root, "chat_list.json")
    with open(the_path) as f:
        json_chat_list = json.loads(f.read())
    return json_chat_list


@app.route('/chat_load', methods=['POST'])
def chat_load():
    chat_name = request.json.get('chatName')
    # Here you can load the chat from the JSON file based on chat_name
    # For demonstration, let's assume loading from a static JSON file
    chat_file_path = os.path.join(app_root, "history", f"{chat_name}.json")
    with open(chat_file_path, "r") as f:
        chat_data = json.loads(f.read())
    return jsonify(chat_data)


@app.route('/chat_create')
def chat_create():
    json_chat_list = {}
    json_out = {
        "status": False
    }
    chat_template = {
        "chats": [
            {
                "bot": "Hello Sir! I'm Jynx, The Jenkins Bot!. You may use my help to trigger jobs on Jenkins!"
            }
        ]
    }
    the_path = os.path.join(app_root, "chat_list.json")
    with open(the_path) as f:
        json_chat_list = json.loads(f.read())
    if json_chat_list != {}:
        json_chat_list["chat_count"] += 1
        json_chat_list["chatList"].append(f"chat_{json_chat_list['chat_count']}")
        with open(the_path, "w") as f:
            f.write(json.dumps(json_chat_list, indent=2))
        with open(os.path.join(app_root, "history", f"chat_{json_chat_list['chat_count']}.json"), "w+") as f:
            f.write(json.dumps(chat_template, indent=2))
        json_out.update({
            "status": True,
            "chat_count": json_chat_list["chat_count"],
            "chat_name": f"chat_{json_chat_list['chat_count']}"
        })
    return json_out
