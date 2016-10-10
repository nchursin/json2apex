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

# TODO: Make another command to launch class renaming. And one more for actual class renaming. Then fire them recursively

class JsonToApexCommand(sublime_plugin.TextCommand):
	apexClassView = {}
	classList = []

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
		self.classList = ["API", "Root_object"]
		self.classList += list(converter.formedClasses.values())
		print(self.classList)
		self.apexClassView = sublime.active_window().new_file()
		self.apexClassView.set_syntax_file('Packages/MavensMate/sublime/lang/Apex.sublime-syntax')
		self.apexClassView.insert(edit, 0, "\n" + gen)

		# self.apexClassView.sel().clear()
		# s = self.classList[2]
		# matches = self.apexClassView.find_all(s)
		# self.apexClassView.sel().add_all(matches)
		self.renameClass()
		
		# print(matches)

		del(converter)

	def renameClass(self):
		args = {
			'classList': self.classList
		}
		print(args)
		edit = self.apexClassView.begin_edit(0, '')
		self.apexClassView.run_command('launch_class_renaming', args)

class LaunchClassRenamingCommand(sublime_plugin.TextCommand):
	apexView = {}
	classList = []
	oldClassName = ''

	def run(self, edit, classList):
		self.apexView = self.view
		self.classList = classList
		curWin = self.apexView.window()
		self.oldClassName = self.classList.pop(0)

		matches = self.apexView.find_all(self.oldClassName)
		self.apexView.sel().clear()
		self.apexView.sel().add_all(matches)

		curWin.show_input_panel('Rename ' + self.oldClassName, self.oldClassName, self.rename, None, None)

	def rename(self, newName):
		args = {
			'oldClassName': self.oldClassName,
			'newClassName': newName,
			'classList': self.classList
		}
		self.apexView.run_command('rename_apex_class', args)

class RenameApexClassCommand(sublime_plugin.TextCommand):
	def run(self, edit, oldClassName, newClassName, classList):
		matches = self.view.find_all(oldClassName)
		reg_end = 0
		for m in matches:
			cur_m = self.view.find(oldClassName, reg_end)
			reg_end = m.end()
			self.view.replace(edit, cur_m, newClassName)
		if(0 < len(classList)):
			args = {
				'classList': classList
			}
			self.view.run_command('launch_class_renaming', args)