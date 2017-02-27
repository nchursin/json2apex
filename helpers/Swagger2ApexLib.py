import sys
import os
import json
import datetime
from PatternClass import Pattern as Pattern
from TemplateHelper import Template as Template
from TemplateHelper import TemplateArgs as TemplateArgs
import os.path, imp, json
# import sublime, sublime_plugin

template_extension = '.tmp'
template_dir = 'templates/RestResourse/'
template_path = 'RestResourse/'
apexrest = '/services/apexrest'
defaultClassName = 'RestAPIClass'
slash = '/'
definitions_const = '#/definitions/'
inner_classes_access = 'private'

templates = {
	'classTemplate': template_path + 'classTemplate',
	'methodCaller': template_path + 'methodCaller',
	'methodHandler': template_path + 'methodHandler',
	'pathParamParser': template_path + 'pathParamParser',
	'retrieveGetParam': template_path + 'retrieveGetParam',
	'retrievePathParam': template_path + 'retrievePathParam',
}

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
	'_var': '{{',
	'_code': '{${',
	'_end': '}}'
}

def parseSchemaForPaths(schema_object):
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
				if var_name not in processed_paths:
					args = TemplateArgs()
					args.addVar('pathParamName', var_name)
					args.addVar('pathParamNumber', i)
					paramParserTemplate = Template(templates['pathParamParser'])
					paramParserTemplate.addArgs(args)
					retrievePathParamTemplate = Template(templates['retrievePathParam'])
					retrievePathParamTemplate.addArgs(args)
					processed_paths.append(var_name)
					parsers.append( paramParserTemplate.compile() )
					retrievers.append( retrievePathParamTemplate.compile() )
				i += 1
	return parsers, retrievers
					
def parseSchemaForMethods(schema_object):
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
			args = TemplateArgs()
			args.addVar('method', method.upper())
			methodHandlerTemplate = Template(templates['methodHandler'])
			methodHandlerTemplate.addArgs(args)
			methodCallerTemplate = Template(templates['methodCaller'])
			methodCallerTemplate.addArgs(args)
			handlers.append( methodHandlerTemplate.compile() )
			callers.append( methodCallerTemplate.compile() )
	return callers, handlers

def parseSchemaForDefinitions(schema_object):
	if 'definitions' not in schema_object:
		return []
	definitions = schema_object['definitions']
	code = []
	for className, defin in definitions.items():
		gen = parseDefintion(defin, className)
		code.append( gen )
	return code

def parseDefintion(definition, def_name):
	pattern = Pattern(def_name, inner_classes_access)
	if 'allOf' in definition:
		parents = definition['allOf']
		for p in parents:
			if '$ref' in p:
				ext = p['$ref']
				ext = ext.replace(definitions_const, '')
				if slash in ext:
					print ('Impossibru!!! Slash found in definition link after removing "#/definitions/"')
				else:
					pattern.addParentClass(ext)
			else:
				if 'object' == p['type']:
					addObjectToPattern(pattern, p)
	elif 'object' == definition['type']:
		addObjectToPattern(pattern, definition)
	return pattern.generateCode('\t')

def addObjectToPattern(pattern, definition):
	for var_name, var_props in definition['properties'].items():
		pattern.addPublicProperty( var_props['type'].capitalize(), var_name )

def parseSchema(schema_object):
	apexrest_start = schema_object['basePath'].find(apexrest)
	base_path = schema_object['basePath'][(apexrest_start + len(apexrest)):]
	class_template = Template(templates['classTemplate'])
	class_template.addVar('basePath', base_path)
	class_template.addVar('ResourseClassName', defaultClassName)
	parsers, retrievers = parseSchemaForPaths(schema_object)
	callers, handlers = parseSchemaForMethods(schema_object)
	predefined_classes = parseSchemaForDefinitions(schema_object)
	class_template.addVar('pathParamParsers', '\n'.join(parsers))
	class_template.addVar('paramRetrievers', '\n'.join(retrievers))
	class_template.addVar('methodCallers', '\n'.join(callers))
	class_template.addVar('methodHandlers', '\n'.join(handlers))
	class_template.addVar('methodHandlers', '\n'.join(handlers))
	class_template.addVar('definitionClasses', '\n'.join(predefined_classes))

	apex_code = class_template.compile()
	# print('\n\n>>><<<\n\n')
	print(apex_code)
