# Integration Apex Class generating tool.
# Receives sample json message
# Generates Apex Class based on it
import sys
import os
import json
import datetime
# import JSON2ApexLib
import Swagger2ApexLib

sample_msg = 'example_GoogleGeocode.json'
smaple_schema = 'example_schema.json'

# read_from = sample_msg
read_from = smaple_schema

pattern = {}

# print datetime.datetime.now()

content = ''
with open(read_from) as f:
    content = f.read()
api_object = json.loads(content)

# JSON2ApexLib.generateFromSample(api_object)
Swagger2ApexLib.parseSchema(api_object)