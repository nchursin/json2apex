import sys
import os
import json
import datetime
from PatternClass import Pattern as Pattern
import os.path, imp, json
# import sublime, sublime_plugin

template_extension = '.tmp'
template_dir = 'templates/RestResourse/'
apexrest = '/services/apexrest'
defaultClassName = 'RestAPIClass'
slash = '/'
definitions = '#/definitions/'

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
	'_var': '{{',
	'_code': '{${',
	'_end': '}}'
}

def getTemplateCode(template_name):
	path_to_template = template_dir + template_name + template_extension
	content = None
	with open(path_to_template) as f:
		content = f.read()
	return content

def compileCode(code, code_locals):
	code_pure = code.replace(TEMPLATE_CONSTS['_code'],'').replace(TEMPLATE_CONSTS['_end'],'')
	code_pure = 'output = ' + code_pure
	compiled = compile(code_pure, '<string>', 'exec')
	exec(compiled, {}, code_locals)
	return code_locals['output']

def findCodeOccurence(template):
	code_end_length = len(TEMPLATE_CONSTS['_end'])
	code_start = template.find(TEMPLATE_CONSTS['_code'])
	template_replace = template[code_start:]
	code_end = code_start + template_replace.find(TEMPLATE_CONSTS['_end']) + code_end_length
	code_occurence = template[code_start:code_end]
	return code_occurence

# template_args = {
# 	code_args:{
# 		name: value
# 	},
# 	template_vars:{
# 		name: value
# 	},
# }

def compileTemplate(template_name, template_args, debug=False):
	template = getTemplateCode(template_name)
	code = findCodeOccurence(template)
	while code:
		template = template.replace(code, compileCode(code, template_args['code_args']))
		code = findCodeOccurence(template)
	for name, placeholder in TEMPLATE_CONSTS.items():
		if name in template_args['template_vars']:
			template = template.replace(placeholder, str(template_args['template_vars'][name]))
	if(debug):
		print('template >> ', template)
	return template

def parseSchemaForPaths(schema_object, template):
	paths = schema_object['paths']
	processed_paths = []
	parsers = []
	retrievers = []
	for p, path_def in paths.items():
		path = p
		if slash == path[0]:
			path = path[1:]
		if path:
			i = 0
			path_list = path.split(slash)
			for part in path_list:
				if '{' in part:
					var_name = part.replace('{','').replace('}','')
				else:
					var_name = 'Part' + str(i)
					# required = False
					# for param in path_def['parameters']:
					# 	if var_name == param['name']:
					# 		required = param['required'];
					# 		break
				if var_name in processed_paths:
					i += 1
					continue
				template_vars = {
					'pathParamName': var_name,
					'pathParamNumber': i
				}
				code_args = {}
				template_args = {
					'code_args': code_args,
					'template_vars': template_vars
				}
				processed_paths.append(var_name)
				parsers.append( compileTemplate( 'pathParamParser', template_args ) )
				retrievers.append( compileTemplate( 'retrievePathParam', template_args ) )
				i += 1
	return parsers, retrievers
					
def parseSchemaForMethods(schema_object, template):
	paths = schema_object['paths']
	processed_paths = []
	handlers = []
	callers = []
	for p, path_def in paths.items():
		for method in path_def:
			if method in processed_paths:
				continue
			processed_paths.append(method)
			template_vars = {
				'method': method.upper()
			}
			template_args = {
				'code_args': {},
				'template_vars': template_vars
			}
			handlers.append( compileTemplate( 'methodHandler', template_args ) )
			callers.append( compileTemplate( 'methodCaller', template_args ) )
	return callers, handlers

# def parseSchemaForDefinitions(schema_object, template):
# 	if 'definitions' in schema_object:
# 		return None
# 	definitions = schema_object['definitions']
# 	for className, defin in definitions:
# 		if 'object' == defin['type']:
# 			pass

def parseSchema(schema_object):
	apexrest_start = schema_object['basePath'].find(apexrest)
	base_path = schema_object['basePath'][(apexrest_start + len(apexrest)):]
	template_vars = {
		'basePath': base_path,
		'ResourseClassName': defaultClassName
	}
	template_args = {
		'code_args': {},
		'template_vars': template_vars
	}
	template = compileTemplate('classTemplate', template_args)
	parsers, retrievers = parseSchemaForPaths(schema_object, template)
	callers, handlers = parseSchemaForMethods(schema_object, template)
	template = template.replace( TEMPLATE_CONSTS['pathParamParsers'], '\n'.join(parsers) )
	template = template.replace( TEMPLATE_CONSTS['paramRetrievers'], TEMPLATE_CONSTS['paramRetrievers'] + '\n' + '\n'.join(retrievers) )
	template = template.replace( TEMPLATE_CONSTS['methodCallers'], '\n'.join(callers) )
	template = template.replace( TEMPLATE_CONSTS['methodHandlers'], '\n'.join(handlers) )
	# print('\n\n>>><<<\n\n')
	print(template)
