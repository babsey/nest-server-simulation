#!/bin/bash

# NEST enviroment
source /opt/nest/bin/nest_vars.sh

# NEST simulation server
python3 main.py -H 0.0.0.0 -p 5000
