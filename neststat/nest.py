import json
import requests
import time

from datetime import datetime
from pymongo import MongoClient
from bson import json_util

NESTSTAT_KEYS = ["nest.target_temperature_f",
                 "nest.ambient_temperature_f",
                 "nest.humidity",
                 "nest.is_online",
                 "wunderground.current_observation.temp_f",
                 "wunderground.current_observation.feelslike_f",
                 "wunderground.current_observation.wind_mph",
                 "wunderground.current_observation.wind_gust_mph",
                 "wunderground.current_observation.precip_today_in",
                 "wunderground.current_observation.pressure_in"]


def count(name, value):
    unix_epoch_timestamp = int(time.time())
    metric_type = 'count'
    metric_name = name

    print('MONITORING|{0}|{1}|{2}|{3}'.format(unix_epoch_timestamp, value, metric_type, metric_name))


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


def log_values(neststat):
    """ Log the values we care about """
    flat = flatten_json(neststat)

    for key in NESTSTAT_KEYS:
        value = flat.get(key)
        try:
            count(key, int(value))
        except ValueError:
            # Working with a non int value.. likely "True/False"
            if value == "True":
                count(key, "1")
            else:
                count(key, "0")


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def run(nest_host, nest_key, nest_device, wunderground_host, wunderground_key, wunderground_station, connect_str):
    # Query Data
    nest = get_nest_json(nest_host, nest_key, nest_device)
    wunderground = get_wunderground(wunderground_host, wunderground_key, wunderground_station)

    # Merge Data
    neststat = {'time': datetime.utcnow(), 'nest': nest, 'wunderground': wunderground}

    # Log Data
    log_values(neststat)

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
