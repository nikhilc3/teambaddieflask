from flask import Flask, render_template, url_for, redirect, Blueprint
from contextlib import nullcontext
from flask_restful import Api, Resource
import requests
import time
import random
import string
import json

app = Flask(__name__)
pass_api = Blueprint('pass_api', __name__, url_prefix='/api/pass')
api = Api(pass_api)
app.register_blueprint(pass_api)

last_run = None

def updateTime():
    global last_run
    try: last_run
    except: last_run = None

    if last_run is None:
        last_run = time.time()
        return True

    elapsed = time.time() - last_run
    if elapsed > 86400:
        last_run = time.time()
        return True

    return False

def getPassAPI(length=3):
    password = []
    url = "https://random-words5.p.rapidapi.com/getMultipleRandom"
    querystring = {"count": str(length)}
    headers = {
        "X-RapidAPI-Key": "f0aeb431bamshc18b522b64e7383p102f67jsnea4673acfc55",
        "X-RapidAPI-Host": "random-words5.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    words = response.json()
    password += words
    password += [random.choice(string.ascii_letters + string.digits) for i in range(2)]
    random.shuffle(password)
    response = ''.join(password)
    return response

class PassAPI:
    class _Read(Resource):
        def get(self):
            return getPassAPI()

    api.add_resource(_Read, '/')

def save_to_json(password):
    # open the JSON file in write mode
    with open('passwords.json', 'w') as f:
        # write the password to the file as a JSON object
        json.dump({"password": password}, f)

# call the function to save the password to the JSON file
save_to_json(getPassAPI(5))

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/hii')
def home():
    return render_template('hii.html')
# Link to home page
