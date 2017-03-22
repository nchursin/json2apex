import sys
import os
import json
import datetime
from PatternClass import Pattern as Pattern
from TemplateHelper import Template as Template
from TemplateHelper import TemplateArgs as TemplateArgs
import os.path, imp, json

restresource_template_path = 'RestResourse/'
other_templates_path = 'other/'
apexrest = '/services/apexrest'
defaultClassName = 'RestAPIClass'
slash = '/'
definitions_const = '#/definitions/'
inner_classes_access = 'private'

templates = {
	'classTemplate': restresource_template_path + 'classTemplate',
	'methodCaller': restresource_template_path + 'methodCaller',
	'methodHandler': restresource_template_path + 'methodHandler',
	'pathParamParser': restresource_template_path + 'pathParamParser',
	'retrieveGetParam': restresource_template_path + 'retrieveGetParam',
	'retrievePathParam': restresource_template_path + 'retrievePathParam',
	'urlValidator': restresource_template_path + 'urlValidator',
	'queryParamGetter': restresource_template_path + 'queryParamGetter',
	'OptionSet': other_templates_path + 'SetConstDefinition',
}

def parseSchemaForPaths(schema_object):
	paths = schema_object['paths']
	processed_paths = []
	parsers = []
	retrievers = []
	path_options = {}
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
					if var_name not in path_options:
						path_options[var_name] = []
					if part not in path_options[var_name]:
						path_options[var_name].append(part)
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
	return parsers, retrievers, path_options

def createPathValidatorsFromOptions(path_options):
	set_name_template = '{replace}_OPTIONS'
	access = 'private'
	object_type = 'String'
	sets = []
	validators = []
	for var_name in path_options:
		path_options[var_name] = list(map(lambda el: "'" + el + "'", path_options[var_name]))
		set_name = set_name_template.replace('{replace}', var_name)
		set_template = Template(templates['OptionSet'])
		set_template.addVar('access', access)
		set_template.addVar('objectType', object_type)
		set_template.addVar('setName', set_name)
		set_template.addVar('setValues', path_options[var_name])
		validator_template = Template(templates['urlValidator'])
		validator_template.addVar('set_name', set_name)
		validator_template.addVar('var_name', var_name)
		sets.append('\t' + set_template.compile())
		validators.append(validator_template.compile())
	return sets, validators

def parseParamsFromSchema(schema_object):
	parameters = {
		'query':[
			# {
			# 	'name': '',
			# 	'required': True
			# }
		],
		'body': []
	}
	paths = schema_object['paths']
	for p, path_def in paths.items():
		for method, method_def in path_def.items():
			if 'parameters' in method_def:
				for param in method_def['parameters']:
					if param['in'] in parameters:
						param['path_pattern'] = p
						parameters[param['in']].append(param)
	return parameters

def generateCodeForParameters(schema_object):
	parameters = parseParamsFromSchema(schema_object)
	print('parameters >> ', parameters)
	print("parameters['query'] >> ", parameters['query'])
	query_params = []
	body_defs = []
	for param in parameters['query']:
		print('param >>> ', param)
		query_param_template = Template(templates['queryParamGetter'])
		if 'required' in param:
			required = param['required']
		else:
			required = False
		query_param_template.addVar('required', required)
		if 'type' in param:
			paramType = param['type']
		else:
			paramType = 'String'
		query_param_template.addVar('paramType', param['type'].capitalize())
		query_param_template.addVar('paramName', param['name'])
		if required:
			query_param_template.addVar('urlPattern', param['path_pattern'])
		query_params.append(query_param_template.compile())

	return query_params, body_defs

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
	classes_to_rename = [ defaultClassName ]
	apexrest_start = schema_object['basePath'].find(apexrest)
	base_path = schema_object['basePath'][(apexrest_start + len(apexrest)):]
	class_template = Template(templates['classTemplate'])
	class_template.addVar('basePath', base_path)
	class_template.addVar('ResourseClassName', defaultClassName)
	parsers, retrievers, path_options = parseSchemaForPaths(schema_object)
	sets, urlValidators = createPathValidatorsFromOptions(path_options)
	callers, handlers = parseSchemaForMethods(schema_object)
	predefined_classes = parseSchemaForDefinitions(schema_object)
	query_params, body_defs = generateCodeForParameters(schema_object)

	class_template.addVar('pathParamParsers', '\n'.join(parsers))
	class_template.addVar('possiblePathParamValuesSets', '\n'.join(sets))
	class_template.addVar('urlValidators', '\n'.join(urlValidators))
	class_template.addVar('paramRetrievers', '\n'.join(retrievers))
	class_template.addVar('methodCallers', '\n'.join(callers))
	class_template.addVar('methodHandlers', '\n'.join(handlers))
	class_template.addVar('methodHandlers', '\n'.join(handlers))
	class_template.addVar('definitionClasses', ''.join(predefined_classes))
	class_template.addVar('pathParams', '\n'.join(query_params))

	apex_code = class_template.compile()
	# print('\n\n>>><<<\n\n')
	return apex_code, classes_to_rename
