import imp, os, sys
import sublime

def __init__():
	pass

def load ( moduleDirectories, pluginGlobals ):

	loadignore_file = os.path.abspath(os.path.dirname(__file__)) + '/.loadignore'
	loadorder_file = os.path.abspath(os.path.dirname(__file__)) + '/.loadorder'

	moduleExtensions  = [ "py" ] #▒▒▒  add extensions here to extend module support   ▒▒▒#
	moduleLoader_Name = "loader"
	modulePaths       = {}
	load_ignore		  = []
	load_order		  = []

	content = []
	with open(loadignore_file) as f:
	    content = f.readlines()
	load_ignore = list(map(lambda x: x.replace('\n',''), content))

	content = []
	with open(loadorder_file) as f:
	    content = f.readlines()
	load_order = list(map(lambda x: x.replace('\n',''), content))

	for path in sys.path:
		if path.endswith ( "Sublime Text 3" + os.sep + "Packages" ):
			packagesPath = path
			break


	package_name = os.path.abspath(os.path.dirname(__file__))

	package_name = os.path.relpath(package_name, packagesPath).split(os.sep, 1)[0]

	path_to_package = packagesPath + os.sep + package_name + os.sep

	for file in load_order:
		path_to_file = path_to_package + file
		moduleName = os.path.basename( path_to_file )[ : - len ( os.extsep + 'py' ) ]
		path = path_to_file.replace(os.path.basename( path_to_file ), '')
		fileObject, file, description = imp.find_module( moduleName, [ path ] )
		pluginGlobals[ moduleName ] = imp.load_module ( moduleName, fileObject, file, description )

	for directory in moduleDirectories:
		if packagesPath not in directory:
			modulePaths[directory.replace(package_name + os.sep,'')] = packagesPath + os.sep + directory 
		else:
			modulePaths[directory.replace(packagesPath + os.sep,'')] = directory 


	for index in range ( 0, 2 ): #▒▒▒  loads modules twice to ensure dependencies are updated  ▒▒▒#
		for dir_name, path in modulePaths.items():
			for file in os.listdir ( path ):
				for extension in moduleExtensions:
					if file.endswith ( os.extsep + extension ):
						moduleName = os.path.basename( file )[ : - len ( os.extsep + extension ) ]
						if moduleName != moduleLoader_Name and (dir_name + '.' + moduleName) not in load_ignore:
							fileObject, file, description = imp.find_module( moduleName, [ path ] )
							pluginGlobals[ moduleName ] = imp.load_module ( moduleName, fileObject, file, description )
