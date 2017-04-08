# import yaml
from collections import OrderedDict


class YAMLer():
	def __init__(self):
		pass

	# def ordered_load(self, stream, Loader=yaml.Loader,
	# object_pairs_hook=OrderedDict):
	def ordered_load(self, stream, Loader=None, object_pairs_hook=OrderedDict):
		pass
		# class OrderedLoader(Loader):
		# 	pass
		# def construct_mapping(loader, node):
		# 	loader.flatten_mapping(node)
		# 	return object_pairs_hook(loader.construct_pairs(node))
		# OrderedLoader.add_constructor(
		# 	yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
		# 	construct_mapping)
		# return yaml.load(stream, OrderedLoader)

# usage example:
# ordered_load(stream, yaml.SafeLoader)
