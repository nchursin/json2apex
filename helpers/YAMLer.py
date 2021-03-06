from . import pyyaml as yaml
from collections import OrderedDict


class YAMLer():
	def __init__(self):
		pass

	# def ordered_load(self, stream, Loader=None, object_pairs_hook=OrderedDict):
	def ordered_load(self, stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
		class OrderedLoader(Loader):
			pass

		def construct_mapping(loader, node):
			loader.flatten_mapping(node)
			return object_pairs_hook(loader.construct_pairs(node))

		OrderedLoader.add_constructor(
			yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
			construct_mapping)

		result = yaml.load(stream, OrderedLoader)
		print('yaml.load(stream) >> ', yaml.load(stream))

		return result

# usage example:
# ordered_load(stream, yaml.SafeLoader)
