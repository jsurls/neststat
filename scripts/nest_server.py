import os
import json
from flask import Flask

app = Flask(__name__)


@app.route("/devices/thermostats/<device>")
def get_thermostat_data(device):
    with open("../sample/sample_nest_response.json") as data_file:
        data = json.load(data_file)
        return json.dumps(data)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
