from flask import Flask, request
import json

app = Flask(__name__)

admins = {
    "Morgandri1": {
        "password": "W!ngnut33",
    }
}

@app.route('/')
def example():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data

@app.route("/items/")
def get():
    unique_id = request.args.get('UID')
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
        return data[unique_id]
    except KeyError:
        return create(unique_id)

def create(UID):
    if UID == None:
        return "No UID provided"
    with open("data.json", "r") as f:
        data = json.load(f)
    data[UID] = {"id": UID, "paid": False, "nuke": False}
    with open("data.json", "w") as f:
        json.dump(data, f)
    return data[UID]

@app.route("/update/")
def update():
    unique_id = request.args.get('UID')
    if unique_id == None:
        return "No UID provided"
    with open("data.json", "r") as f:
        data = json.load(f)
    try:
        data[unique_id]["paid"] = True
        with open("data.json", "w") as f:
            json.dump(data, f)
        return data[unique_id]
    except KeyError:
        return create(unique_id)

@app.route("/routes/")
def routes():
    return """
Routes: <br>
/items/?UID - Get item by UID <br>
/update/?UID - Update item to 'paid' by UID <br>
/routes/ - Get routes <br>
/nuke/?UID&user&pass - Nuke item by UID <br>
/ - get all item data
"""

@app.route("/nuke/")
def nuke():
    user = request.args.get('user')
    password = request.args.get('pass')
    UID = request.args.get('UID')
    try:
        if password == admins[user]["password"]:
            with open("data.json", "r") as f:
                data = json.load(f)
            data[UID]["nuke"] = True
            with open("data.json", "w") as f:
                json.dump(data, f)
            return "Nuked"
        else:
            with open("log.json", "r") as f:
                data = json.load(f)
            try:
                data[user]["attempts"] += 1
            except KeyError:
                data[user] = {"attempts": 1}
            return "Incorrect password"
    except KeyError:
        return "Invalid user"

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080)