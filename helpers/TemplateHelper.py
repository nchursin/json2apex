import os
import os.path
import re
from .FileReader import FileReader as FR

from . import logger
log = logger.get(__name__)

template_dir = os.path.abspath(os.path.dirname(__file__)) + '/templates/'
template_extension = '.template'

TEMPLATE_CONSTS = {
	'_var': '{{',
	'_code': '{${',
	'_end': '}}',
	'_code_end': '}$}'
}


def __init__():
	pass

# template_args = {
# 	template_vars:{
# 		name: value
# 	},
# }


class Template():
	"""Arguments to be passed to template"""
	def __init__(self, template_name):
		self.template_name = template_name
		self.template_args = TemplateArgs()
		self.output = ''
		self.getTemplateCode()

	def getTemplateCode(self):
		# content = TG.getTemplates()[self.template_name]

		path_to_template = template_dir + self.template_name + template_extension
		content = FR.read(path_to_template)
		# content = None
		# with open(path_to_template) as f:
		# 	content = f.read()
		self.template = content

	def addVar(self, var_name, var_value):
		self.template_args.addVar(var_name, var_value)

	def addCodeArgument(self, var_name, var_value):
		self.template_args.addCodeArgument(var_name, var_value)

	def addArgs(self, template_args):
		for ca_name, ca_value in template_args.template_vars.items():
			self.template_args.template_vars[ca_name] = ca_value
		for var_name, var_value in template_args.template_vars.items():
			self.template_args.template_vars[var_name] = var_value

	def findCodeOccurence(self):
		code_end_length = len(TEMPLATE_CONSTS['_code_end'])
		code_start = self.output.find(TEMPLATE_CONSTS['_code'])
		template_replace = self.output[code_start:]
		code_end = code_start + template_replace.find(
			TEMPLATE_CONSTS['_code_end']) + code_end_length
		code_occurence = self.output[code_start:code_end]
		return code_occurence

	def compileCode(self, code):
		code_locals = self.template_args.template_vars
		code_pure = code.replace(
			TEMPLATE_CONSTS['_code'], '').replace(
			TEMPLATE_CONSTS['_code_end'], '')
		code_pure = 'output = ' + code_pure
		# log.debug('code_pure >>> ' + code_pure)
		compiled = compile(code_pure, '<string>', 'exec')
		exec(compiled, {}, code_locals)
		return code_locals['output']

	def compile(self, debug=False):
		self.output = self.template
		code = self.findCodeOccurence()
		while code:
			self.output = self.output.replace(code, self.compileCode(code))
			code = self.findCodeOccurence()
		template_vars = {}
		pattern = TEMPLATE_CONSTS['_var'] + '\w+' + TEMPLATE_CONSTS['_end']
		template_var_occurences = re.findall(pattern, self.output)
		for var_occ in template_var_occurences:
			key = var_occ.replace(
				TEMPLATE_CONSTS['_var'], '').replace(
				TEMPLATE_CONSTS['_end'], '')
			template_vars[key] = var_occ
		for name, placeholder in template_vars.items():
			if name in self.template_args.template_vars:
				self.output = self.output.replace(
					placeholder, str(self.template_args.template_vars[name]))
			else:
				self.output = self.output.replace(placeholder, '')
		log.debug('before formatting >>> ' + self.output)
		output_splitted = self.output.split('\n')
		self.output = ''
		remove_next_if_empty = False
		for part in output_splitted:
			if re.match(r'^\s*\}{0,1}$', part) and remove_next_if_empty:
				if part.endswith('}'):
					log.debug('to add >>> ' + part)
					if self.checkIfLastLineEmpty(self.output):
						self.output = self.output[:self.output.rindex('\n') + 1]
						self.output += part
					else:
						self.output += part
					remove_next_if_empty = False
				else:
					pass
			else:
				# if self.checkIfLastLineEmpty(self.output):
				log.debug('to add >>> ' + '\n' + part)
				self.output += '\n' + part
				remove_next_if_empty = re.match(r'^\s*$', part) or part.endswith('{')
		self.output = ' '.join(
			filter(
				lambda x: not re.match(r'^\s*$', x),
				self.output.split(' ')))
		self.output = self.output[1:]
		return self.output

	def checkIfLastLineEmpty(self, text):
		to_check = self.output[self.output.rindex('\n') + 1:]
		return re.match(r'^\s*$', to_check)


class TemplateArgs():
	"""Arguments to be passed to template"""
	def __init__(self):
		self.template_vars = {}

	def addVar(self, var_name, var_value):
		self.template_vars[var_name] = var_value

	def addCodeArgument(self, var_name, var_value):
		self.template_vars[var_name] = var_value
