[![Build Status](https://travis-ci.org/jsurls/neststat.svg?branch=master)](https://travis-ci.org/jsurls/neststat)
# neststat
Capture Nest Thermostat Statistics


## Developer Setup
```
# Install virtualenv and virtualenvwrapper
pip install virtualenv virtualenvwrapper

# Create venv
virtualenv venv

# Source env
source venv/bin/activate

# Install pybuilder and gitpython
pip install pybuilder gitpython

# Install dependencies
pyb install_dependencies

# Build
pyb

# Start dependencies
docker-compose up

# Run
python src/main/python/nest.py
```


## Background
The Nest thermostat has provided all sorts of revealing details about our AC and Heating.

My curiosity kicked in to see what else could I learn that the Nest doesn't provide. In doing so,
 I attempted to answer the following:
 - How well does it stay at target temperature?
 - How does the outside weather affect this?
 - Can pre-cooling help? And at what outside temps?
 - How does humidity (indoor and outdoor) play a role?
 
The Nest already provides a historical view but only answers *how many hours it ran*.

## What this repo does
nest.py does the following:
 - Get thermostat data from Nest
 - Get local Wunderground data from a PWS
 - Merge and timestamp data
 - Print metrics (for Datadog to consume via Cloudwatch Logs)
 - Store in a Datastore
 
## Building
This repo is built using [pybuilder](http://pybuilder.github.io/)
```
pyb
```

## Deploying
Build a new artifact and upload to S3
```
pyb deploy
```

Update your lambda to point to the new artifact
```
pyb update_lambda
```
