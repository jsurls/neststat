# neststat
Capture Nest Thermostat Statistics


## Developer Setup
```
# Install virtualenv and virtualenvwrapper
pip install virtualenv
pip install virtualenvwrapper
 
# Start dependencies
docker-compose up

# Run App
python nest.py
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
 - Store in a Datastore
 
## Building
```
build.sh
```

## Deploying
Upload to AWS Lambda and run on an interval. Currently manually done.