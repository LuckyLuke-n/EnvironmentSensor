#!/bin/bash

# Change to the directory where your virtual environment and script are located
cd ~/Sources/Tempsensor

# Activate the virtual environment
source tempsensorenv/bin/activate

# Start the Python script using nohup
cd src
nohup python3 envsensor.py &