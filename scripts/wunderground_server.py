import os
import json
from flask import Flask

app = Flask(__name__)


@app.route("/api/<apikey>/conditions/q/pws:<station>.json")
def get_history(apikey, station):
    with open("../sample/sample_current_conditions_response.json") as data_file:
        data = json.load(data_file)
        return json.dumps(data)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5001.
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
