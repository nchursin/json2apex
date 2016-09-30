import sys
import os
import json
import datetime
from PatternClass import Pattern as Pattern
import os.path, imp, sublime, sublime_plugin, json

types = {
	float: 'Double',
	int: 'Integer',
	bool: 'Boolean',
	str: 'String',
	bytes: 'String',
	None: 'String',
	'int': 'Integer',
	'bool': 'Boolean',
	'boolean': 'Boolean',
	'string': 'String',
	'float': 'Double'
}

# class_pattern = Pattern()

formedClasses = {}
classReplacers = {}

def mergeDicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z

def checkIsClassGenerated(api_object, className):
	# print json.dumps(api_object)
	props = list(api_object.keys())
	props.sort()
	props = ','.join(props)
	# print props
	if props in formedClasses:
		return formedClasses[props]
	else:
		formedClasses[props] = className
		return None

def getClassName(prop, key):
	className = ''
	if dict == type(prop):
		className = key.capitalize() + 'Class'
	# elif str == type(prop):
	# 	className = types[type(prop)]
	elif type(None) == type(prop):
		className = 'String'
	elif list == type(prop):
		className = 'List<' + getClassName(prop[0], key) + '>'
	else:
		className = types[type(prop)]
	return className

def generatePatternFromSample (api_object, cName):
	# TODO: change pattern structure to implement the above sample
	pattern = Pattern(cName, 'public', False)
	dics = {}
	for key, value in api_object.items():
		className = getClassName(value, key)
		className_str = str(className)
		pattern.addPublicProperty(className, key)
		if dict == type(value):
			dics[key] = value
		if className_str.startswith('List<'):
			if dict == type(value[0]):
				dics[className] = value[0]

	return {
			'pattern' : pattern,
			'dics' : dics
		}

def generateClass (pattern):
	res = ''
	for key, value in pattern.items():
		for p in value:
			prop = '\n		public ' + key + ' ' + p + ';'
			res += prop
	return res

def generateFromSample (root_object):
	classDfn = 'public class API{\n'
	root_pattern = {}
	first_result = generatePatternFromSample (root_object, 'Root_object')
	dics = first_result['dics']
	root_pattern['Root_object'] = first_result['pattern'].class_pattern
	classDfn += first_result['pattern'].generateCode('\t')
	while 0 != len(dics.keys()):
		key, value = dics.popitem()
		className = key.capitalize() + 'Class'
		classCheck = checkIsClassGenerated(value, className)
		if None == classCheck:
			genRes = generatePatternFromSample(value, className)
			root_pattern[key] = genRes['pattern'].class_pattern

			classDfn += genRes['pattern'].generateCode('\t')

			dics = mergeDicts(dics, genRes['dics'])
		else:
			if classCheck not in classReplacers:
				classReplacers[classCheck] = []
			classReplacers[classCheck].append(className)


	# print classReplacers

	for key, value in classReplacers.items():
		className = key
		for c in value:
			oldClassName = c
			classDfn = classDfn.replace(' ' + oldClassName + ' ', ' ' + className + ' ')

	classDfn += '\n}\n'

	# print root_pattern
	# print 'formed pattern >> '
	# print json.dumps(root_pattern)
	# print 'generated code >> '
	# print classDfn
	return classDfn


# def generateFromSchema(schema):
# 	for key, value in schema.items():
# 		print '\tpublic ' + types[value['type']] + ' ' + key + ';'