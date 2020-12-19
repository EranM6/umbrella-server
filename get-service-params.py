#!/usr/bin/env python
from utils import generate_file
import os
import sys

env = os.getenv('env')
service = os.getenv('service')
if not env or not service:
    print("you must set env as environment variable")
    sys.exit(1)

temp_values = "values-temp.yaml"

error = generate_file(service, env, temp_values)

if error:
    print("Error: {}".format(error))
else:
    print("{} was created".format(temp_values))
