import sys
import os
import json
import datetime
import os.path, imp, json

template_dir = 'templates/'
template_extension = '.tmp'

TEMPLATE_CONSTS = {
	'basePath': '{{basePath}}',
	'ResourseClassName': '{{ResourseClassName}}',
	'methodCallers': '{{methodCallers}}',
	'methodHandlers': '{{methodHandlers}}',
	'pathParamParsers': '{{pathParamParsers}}',
	'paramRetrievers': '{{paramRetrievers}}',
	'paramName': '{{paramName}}',
	'pathParamName': '{{pathParamName}}',
	'method': '{{method}}',
	'pathParamNumber': '{{pathParamNumber}}',
	'definitionClasses': '{{definitionClasses}}',
	'notdefinedClasses': '{{notdefinedClasses}}',
	'getParamParsers': '{{getParamParsers}}',
	'bodyParsers': '{{bodyParsers}}',
	'_var': '{{',
	'_code': '{${',
	'_end': '}}'
}

# template_args = {
# 	code_args:{
# 		name: value
# 	},
# 	template_vars:{
# 		name: value
# 	},
# }

class Template():
	"""Template compiler"""
	def __init__(self, template_name):
		self.template_name = template_name
		self.template_args = TemplateArgs()
		self.output = ''
		self.getTemplateCode()

	def getTemplateCode(self):
		path_to_template = template_dir + self.template_name + template_extension
		content = None
		with open(path_to_template) as f:
			content = f.read()
		self.template = content

	def addVar(self, var_name, var_value):
		self.template_args.addVar(var_name, var_value)

	def addCodeArgument(self, var_name, var_value):
		self.template_args.addCodeArgument(var_name, var_value)

	def addArgs(self, template_args):
		for ca_name, ca_value in template_args.code_args.items():
			self.template_args.code_args[ca_name] = ca_value
		for var_name, var_value in template_args.template_vars.items():
			self.template_args.template_vars[var_name] = var_value

	def findCodeOccurence(self):
		code_end_length = len(TEMPLATE_CONSTS['_end'])
		code_start = self.output.find(TEMPLATE_CONSTS['_code'])
		template_replace = self.output[code_start:]
		code_end = code_start + template_replace.find(TEMPLATE_CONSTS['_end']) + code_end_length
		code_occurence = self.output[code_start:code_end]
		return code_occurence

	def compileCode(self, code):
		code_locals = self.template_args.code_args
		code_pure = code.replace(TEMPLATE_CONSTS['_code'],'').replace(TEMPLATE_CONSTS['_end'],'')
		code_pure = 'output = ' + code_pure
		compiled = compile(code_pure, '<string>', 'exec')
		exec(compiled, {}, code_locals)
		return code_locals['output']

	def compile(self, debug=False):
		self.output = self.template
		code = self.findCodeOccurence()
		while code:
			self.output = self.output.replace(code, self.compileCode(code))
			code = self.findCodeOccurence()
		for name, placeholder in TEMPLATE_CONSTS.items():
			if(debug):
				print('name >> ', name)
				print('placeholder >> ', placeholder)
				print('name in self.template_args.template_vars >> ', name in self.template_args.template_vars)
				if name in self.template_args.template_vars:
					print('str(self.template_args.template_vars[name]) >> ', str(self.template_args.template_vars[name]))
			if name in self.template_args.template_vars:
				self.output = self.output.replace(placeholder, str(self.template_args.template_vars[name]))
		if(debug):
			print('template >> ', self.output)
		return self.output


class TemplateArgs():
	"""Arguments to be passed to template"""
	def __init__(self):
		self.code_args = {}
		self.template_vars = {}

	def addVar(self, var_name, var_value):
		self.template_vars[var_name] = var_value

	def addCodeArgument(self, var_name, var_value):
		self.code_args[var_name] = var_value
		