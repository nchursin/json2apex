# Integration Apex Class generating tool.
# Receives sample json message
# Generates Apex Class based on it
import sys
import os
import json
import datetime
# import JSON2ApexLib
# import Swagger2ApexLib
import PatternClass

sample_msg = 'example_sample.json'
sample_schema = 'example_schema.json'
sample_pattern = 'example_pattern.json'

# read_from = sample_msg
# read_from = sample_schema
read_from = sample_pattern

pattern = {}

# print datetime.datetime.now()

content = ''
with open(read_from) as f:
    content = f.read()
api_object = json.loads(content)

# print(JSON2ApexLib.SampleConverter().generateFromSample(api_object))
# print(Swagger2ApexLib.parseSchema(api_object))
print(PatternClass.Pattern.fromSchema('PatternClass', api_object).generateCode())