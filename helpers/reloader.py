import sys
import imp

from . import logger
log = logger.get(__name__)

# Dependecy reloader stolen from the Emmet plugin
parent = 'json2Apex.helpers'

reload_mods = []
def fill_reload_mods():
    reload_mods = []
    for mod in sys.modules:
        if mod.startswith(parent) and sys.modules[mod] is not None:
            reload_mods.append(mod)
    return reload_mods

fill_reload_mods()

mods_load_order = [
    'logger',
    'templates',
    'FileReader',
    'YAMLer',
    'TemplateHelper',
    'PatternClass',
    'JSON2ApexLib',
    'reloader',
]

mods_load_order = [parent + '.' + mod for mod in mods_load_order]

def reload():
    reload_mods = fill_reload_mods()
    log.debug('reloading')
    for mod in mods_load_order:
        log.debug('mod >> ' + mod)
        if mod in reload_mods:
            log.debug('reload mod >> ' + mod)
            imp.reload(sys.modules[mod])
