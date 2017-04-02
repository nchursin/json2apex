def getTemplates():
	return {
		'ClassProperty': "{{access}} {${'static' if static else ''}$} {{valueType}} {{propName}}{${' { get; set; }' if createGetSet else ';'}$}",
		'Method': '''{${ '// {{comment}}' if comment else '' }$}
{{access}} {${'static' if static else ''}$} {{returnType}} {{methodName}} ({{methodArguments}}){
	{${'' if 'void' == returnType else '{{returnType}} result;'}$}
	{${'// TODO: {{todo_comment}}' if todo_comment else ''}$}
	{${'' if 'void' == returnType else 'return result;'}$}
}''',
		'SimpleClassTemplate': '''{{intends}}{{access}} {${'{{classType}}' if classType else ''}$} class {{className}}{${'' if not extends else ' extends {{extends}}'}$}{${'' if not implements else ' implements {{implements}}'}$} {

{${'\n'.join([('	{{intends}}' + prop) for prop in properties])}$}

	{{methods}}
	
{{intends}}}
'''
	}