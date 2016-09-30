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

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")

class TestapexCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		contents = self.view.substr(sublime.Region(0, self.view.size()))
		api_object = json.loads(contents)
		gen = JSON2ApexLib.generateFromSample(api_object)
		newfile = sublime.active_window().new_file()
		newfile.insert(edit, 0, "\n" + gen)
