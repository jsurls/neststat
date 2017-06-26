import json
import requests

from datetime import datetime
from pymongo import MongoClient
from bson import json_util


def get_nest_json(key, device):
    print("[nest] Start: " + str(datetime.utcnow()))
    # Setup URL
    # url = "https://developer-api.nest.com/devices/thermostats/" + device
    url = "http://localhost:5000/devices/thermostats/" + device

    # Setup Headers
    headers = {'Authorization': 'Bearer {0}'.format(key), 'Content-Type': 'application/json'}

    # Request
    initial_response = requests.get(url, headers=headers, allow_redirects=False)

    # Process Redirect
    if initial_response.status_code == 307:
        initial_response = requests.get(initial_response.headers['Location'], headers=headers, allow_redirects=False)

    # Print Response
    print("[nest] Response: " + initial_response.text)

    # Create Dict
    data = json.loads(initial_response.text)

    print("[nest] Stop: " + str(datetime.utcnow()))

    return data


def get_wunderground(wunderground_key, wunderground_station):
    print("[wunderground] Start: " + str(datetime.utcnow()))
    # Setup URL
    # url = "https://developer-api.nest.com/devices/thermostats/" + device
    url = "http://localhost:5001/api/%s/conditions/q/pws:%s.json" % (wunderground_key, wunderground_station)

    # Request
    initial_response = requests.get(url, allow_redirects=False)

    # Process Redirect
    if initial_response.status_code == 307:
        initial_response = requests.get(initial_response.headers['Location'], allow_redirects=False)

    # Print Response
    print("[wunderground] Response : " + initial_response.text)

    # Create Dict
    data = json.loads(initial_response.text)

    print("[wunderground] Stop: " + str(datetime.utcnow()))

    return data


def save(doc):
    """ Saves document to Mongo """
    print("[mongo] Start: " + str(datetime.utcnow()))
    print("[mongo] Saving: " + json.dumps(doc, default=json_util.default))
    client = MongoClient('mongodb://localhost:27017/neststat')
    samples = client.neststat.samples
    doc_id = samples.insert_one(doc).inserted_id
    print("[mongo] response: " + str(doc_id))
    print("[mongo] Stop: " + str(datetime.utcnow()))


def run(nest_key, nest_device, wunderground_key, wunderground_station):
    # Query Data
    nest = get_nest_json(nest_key, nest_device)
    wunderground = get_wunderground(wunderground_key, wunderground_station)

    # Merge Data
    neststat = {'time': datetime.utcnow(), 'nest': nest, 'wunderground': wunderground}

    # Save Data
    save(neststat)


def main():
    # Load Config
    nest_key = "dummy_key"
    nest_device = "dummy_device"
    wunderground_key = "dummy_key"
    wunderground_station = "dummy_station"

    # Run
    run(nest_key, nest_device, wunderground_key, wunderground_station)

if __name__ == '__main__':
    main()
