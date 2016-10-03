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

class SampleConverter:
	formedClasses = {}
	classReplacers = {}

	def __init__(self):
		self.formedClasses = {}
		self.classReplacers = {}

	def mergeDicts (self, x, y):
	    z = x.copy()
	    z.update(y)
	    return z

	def checkIsClassGenerated (self, api_object, className):
		props = list(api_object.keys())
		props.sort()
		props = ','.join(props)
		if props in self.formedClasses:
			return self.formedClasses[props]
		else:
			self.formedClasses[props] = className
			return None

	def getClassName (self, prop, key):
		className = ''
		if dict == type(prop):
			className = key.capitalize() + 'Class'
		elif type(None) == type(prop):
			className = 'String'
		elif list == type(prop):
			className = 'List<' + self.getClassName(prop[0], key) + '>'
		else:
			className = types[type(prop)]
		return className

	def generatePatternFromSample (self, api_object, cName):
		pattern = Pattern(cName, 'public', False)
		dics = {}
		for key, value in api_object.items():
			className = self.getClassName(value, key)
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

	def generateClass (self, pattern):
		res = ''
		for key, value in pattern.items():
			for p in value:
				prop = '\n		public ' + key + ' ' + p + ';'
				res += prop
		return res

	def generateFromSample (self, root_object):
		classDfn = 'public class API\n{\n'
		root_pattern = {}
		first_result = self.generatePatternFromSample(root_object, 'Root_object')
		dics = first_result['dics']
		root_pattern['Root_object'] = first_result['pattern'].class_pattern
		classDfn += first_result['pattern'].generateCode('\t')
		while 0 != len(dics.keys()):
			key, value = dics.popitem()
			className = key.capitalize() + 'Class'
			classCheck = self.checkIsClassGenerated(value, className)
			if None == classCheck:
				genRes = generatePatternFromSample(value, className)
				root_pattern[key] = genRes['pattern'].class_pattern

				classDfn += genRes['pattern'].generateCode('\t')

				dics = self.mergeDicts(dics, genRes['dics'])
			else:
				if classCheck not in self.classReplacers:
					self.classReplacers[classCheck] = []
				self.classReplacers[classCheck].append(className)

		for key, value in self.classReplacers.items():
			className = key
			for c in value:
				oldClassName = c
				classDfn = classDfn.replace(' ' + oldClassName + ' ', ' ' + className + ' ')

		classDfn += '\n}\n'

		return classDfn


# def generateFromSchema(schema):
# 	for key, value in schema.items():
# 		print '\tpublic ' + types[value['type']] + ' ' + key + ';'