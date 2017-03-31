import sys
import imp

from . import logger
log = logger.get(__name__)

# Dependecy reloader stolen from the Emmet plugin
parent = 'json2apex.helpers'

reload_mods = []
for mod in sys.modules:
    if mod.startswith(parent) and sys.modules[mod] is not None:
        reload_mods.append(mod)

mods_load_order = [
    'logger',
    'TemplateHelper',
    'PatternClass',
    'JSON2ApexLib',
]

mods_load_order = [parent + '.' + mod for mod in mods_load_order]


def reload():
    log.debug('reloading')
    for mod in mods_load_order:
        if mod in reload_mods:
            imp.reload(sys.modules[mod])