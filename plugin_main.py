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
		contents = self.view.substr(sublime.Region(0, self.view.size()))
		try:
			api_object = json.loads(contents)
		except ValueError:
			sublime.error_message('Invalid JSON')
		else:
			gen = JSON2ApexLib.generateFromSample(api_object)
			apexClass = sublime.active_window().new_file()
			apexClass.set_syntax_file('Packages/MavensMate/sublime/lang/Apex.sublime-syntax')
			apexClass.insert(edit, 0, "\n" + gen)
