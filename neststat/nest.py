import json
import requests

from datetime import datetime
from pymongo import MongoClient
from bson import json_util


def get_nest_json(nest_host, key, device):
    print("[nest] Start: " + str(datetime.utcnow()))
    # Setup URL
    url = "%s/devices/thermostats/%s" % (nest_host, device)

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


def get_wunderground(wunderground_host, wunderground_key, wunderground_station):
    print("[wunderground] Start: " + str(datetime.utcnow()))
    # Setup URL
    url = "%s/api/%s/conditions/q/pws:%s.json" % (wunderground_host, wunderground_key, wunderground_station)

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


def save(connect_str, doc):
    """ Saves document to Mongo """
    print("[mongo] Start: " + str(datetime.utcnow()))
    print("[mongo] Saving: " + json.dumps(doc, default=json_util.default))
    client = MongoClient(connect_str)
    samples = client.neststat.samples
    doc_id = samples.insert_one(doc).inserted_id
    print("[mongo] response: " + str(doc_id))
    print("[mongo] Stop: " + str(datetime.utcnow()))


def run(nest_host, nest_key, nest_device, wunderground_host, wunderground_key, wunderground_station, connect_str):
    # Query Data
    nest = get_nest_json(nest_host, nest_key, nest_device)
    wunderground = get_wunderground(wunderground_host, wunderground_key, wunderground_station)

    # Merge Data
    neststat = {'time': datetime.utcnow(), 'nest': nest, 'wunderground': wunderground}

    # Save Data
    save(connect_str, neststat)


def main():
    # Load Config
    nest_host = "http://localhost:5000"
    nest_key = "dummy_key"
    nest_device = "dummy_device"

    wunderground_host = "http://localhost:5001"
    wunderground_key = "dummy_key"
    wunderground_station = "dummy_station"

    connect_str = "mongodb://localhost:27017/neststat"

    # Run
    run(nest_host, nest_key, nest_device, wunderground_host, wunderground_key, wunderground_station, connect_str)

if __name__ == '__main__':
    main()
