import imp, os, sys

def __init__():
	pass

def load ( moduleDirectories, pluginGlobals ):

	loadignore_file = os.path.abspath(os.path.dirname(__file__)) + '/.loadignore'

	moduleExtensions  = [ "py" ] #▒▒▒  add extensions here to extend module support   ▒▒▒#
	moduleLoader_Name = "loader"
	modulePaths       = {}
	load_ignore		  = []

	content = []
	with open(loadignore_file) as f:
	    content = f.readlines()
	load_ignore = list(map(lambda x: x.replace('\n',''), content))

	for path in sys.path:
		if path.endswith ( "Sublime Text 3" + os.sep + "Packages" ):
			packagesPath = path
			break

	for directory in moduleDirectories:
		modulePaths[directory.replace('json2Apex/','')] = packagesPath + os.sep + directory 

	for index in range ( 0, 2 ): #▒▒▒  loads modules twice to ensure dependencies are updated  ▒▒▒#
		for dir_name, path in modulePaths.items():
			for file in os.listdir ( path ):
				for extension in moduleExtensions:

					if file.endswith ( os.extsep + extension ):
						moduleName = os.path.basename( file )[ : - len ( os.extsep + extension ) ]
						if moduleName != moduleLoader_Name and (dir_name + '.' + moduleName) not in load_ignore:
							fileObject, file, description = imp.find_module( moduleName, [ path ] )
							pluginGlobals[ moduleName ] = imp.load_module ( moduleName, fileObject, file, description )
