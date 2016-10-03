import sys, os.path, imp, sublime, sublime_plugin, json

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
CODE_DIRS = [
  'helpers',
]
sys.path += [BASE_PATH] + [os.path.join(BASE_PATH, f) for f in CODE_DIRS]

# =======
# reload plugin files on change
# if 'helpers.reloader' in sys.modules:
# 	imp.reload(sys.modules['helpers.reloader'])
if 'helpers.JSON2ApexLib' in sys.modules:
	imp.reload(sys.modules['helpers.JSON2ApexLib'])
if 'helpers.PatternClass' in sys.modules:
	imp.reload(sys.modules['helpers.PatternClass'])
# import helpers.reloader
import helpers.JSON2ApexLib as JSON2ApexLib
import helpers.PatternClass as PatternClass
# print(PatternClass)

class JsonToApexCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		api_object = self.getContent()
		if(api_object is not None):
			self.generateCode(edit, api_object)

	def getContent(self):
		try:
			contents = self.view.substr(sublime.Region(0, self.view.size()))
			api_object = json.loads(contents)
			return api_object
		except ValueError:
			sublime.error_message('Invalid JSON')
			return None

	def generateCode(self, edit, api_object):
		converter = JSON2ApexLib.SampleConverter()
		gen = converter.generateFromSample(api_object)
		apexClass = sublime.active_window().new_file()
		apexClass.set_syntax_file('Packages/MavensMate/sublime/lang/Apex.sublime-syntax')
		apexClass.insert(edit, 0, "\n" + gen)
		del(converter)
			