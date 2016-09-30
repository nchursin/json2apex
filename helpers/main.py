# Integration Apex Class generating tool.
# Receives sample json message
# Generates Apex Class based on it
import sys
import os
import json
import datetime
import JSON2ApexLib

sample_msg = 'example_GoogleGeocode.json'
smaple_schema = 'schema.json'

pattern = {}

# print datetime.datetime.now()

content = ''
with open(sample_msg) as f:
    content = f.read()
api_object = json.loads(content)

# print api_object

JSON2ApexLib.generateFromSample(api_object)

# with open(smaple_schema) as f:
#     content2 = f.read()
# schema = json.loads(content2)

# JSON2Apex.generateFromSchema(schema)