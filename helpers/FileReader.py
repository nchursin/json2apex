import os
import os.path
import zipfile

from . import logger
log = logger.get(__name__)
folder_name = 'helpers'


class FileReader():
	def __init__(self):
		pass

	@classmethod
	def isPackage(cls):
		package_container = os.path.abspath(os.path.dirname(__file__))
		if(package_container.endswith(folder_name)):
			package_container = package_container[:-len(folder_name)]
		if(package_container.endswith(os.sep)):
			package_container = package_container[:-len(os.sep)]
		name, ext = os.path.splitext(package_container)
		return '.sublime-package' == ext, package_container

	@classmethod
	def readFileFromFolder(cls, path):
		with open(path) as f:
			content = f.read()
		return content

	@classmethod
	def readFileFromZip(cls, zip_path, path_inside):
		if path_inside[0] == os.sep:
			path_inside = path_inside[1:]
		archive = zipfile.ZipFile(zip_path, 'r')
		with archive.open(path_inside) as f:
			content = f.read()
		log.debug('content >> ' + content.decode("utf-8"))
		return content.decode("utf-8")

	@classmethod
	def read(cls, path):
		log.debug('path >> ' + path)
		is_pack, pack_container = cls.isPackage()
		log.debug('is_pack >> ' + str(is_pack))
		log.debug('pack_container >> ' + pack_container)
		if is_pack:
			content = cls.readFileFromZip(
				pack_container, path.replace(pack_container, ''))
		else:
			content = cls.readFileFromFolder(path)
		return content
