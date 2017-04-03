
class TemplateGetter():
	def __init__(self):
		pass
		
	def getTemplates():
		return {
			'other/ClassProperty': "{{access}} {${'static' if static else ''}$} {{valueType}} {{propName}}{${' { get; set; }' if createGetSet else ';'}$}",
			'other/Method': "{${ '// {{comment}}' if comment else '' }$}\n\t{{access}} {${'static' if static else ''}$} {{returnType}} {{methodName}} ({{methodArguments}}){\n\t\t{${'' if 'void' == returnType else '{{returnType}} result;'}$}\n\t\t{${'// TODO: {{todo_comment}}' if todo_comment else ''}$}\n\t\t{${'' if 'void' == returnType else 'return result;'}$}\n\t\t}",
			'other/SimpleClassTemplate': "\n{{intends}}{{access}} {${'{{classType}}' if classType else ''}$} class {{className}}{${'' if not extends else ' extends {{extends}}'}$}{${'' if not implements else ' implements {{implements}}'}$} {\n\n{${'\\n'.join([('	{{intends}}' + prop) for prop in properties])}$}\n\n\t\t{{methods}}\n\n{{intends}}}"
		}