import os
import json
# import sublime, sublime_plugin

# {
#   'extends': [],
#   'implements': [],
#   'properties':
#   {
#       'public':
#       {
#           'static':{}
#               'String':[]
#           },
#           'Boolean': []
#       },
#       'private':
#       {
#           'Integer': [],
#           'Decimal': []
#       }
#   },
#   'methods':
#   {
#       'public':
#       {
#           'static':
#           {
#               'void':
#               [
#                   'name': 'methodName',
#                   'arguments':
#                   {
#                       'String': [],
#                       'Integer': []
#                   }
#               ]
#           }
#       }
#   }
# }

interface_methods = {
    'Comparable': {
        'public': {
            'Integer': [
                {
                    'name': 'compareTo',
                    'arguments': {
                        'Object': [
                            'other'
                        ]
                    }
                }
            ]
        }
    }
}

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

class Pattern:
    class_pattern = {}
    name = ''
    access = ''
    abstract = ''

    generated_code = ''

    def __init__(self, name, access='private', abstract=False):
        self.class_pattern = {
            'extends': [],
            'implements': [],
            'properties': {
                'public': {},
                'private': {}
            },
            'methods': {
                'public': {},
                'private': {}
            }
        }
        name_str = str(name)
        if name_str.startswith('List<'):
            name = name_str.replace('List<','').replace('>Class','').capitalize()
            name = rreplace(name, 'class', 'Class', 1)
        self.name = name
        self.access = access
        self.abstract = abstract

    def toJson(self):
        return json.dumps(self.class_pattern)

    def addExtends(self, class_name):
        self.class_pattern['extends'].append(class_name)

    def addInterface(self, interface_name):
        self.class_pattern['implements'].append(interface_name)
        if interface_name in interface_methods:
            for access_level in interface_methods[interface_name]:
                for return_type in interface_methods[interface_name][access_level]:
                    if return_type not in self.class_pattern['methods'][access_level]:
                        self.class_pattern['methods'][access_level][return_type] = {}
                    self.class_pattern['methods'][access_level][return_type] += interface_methods[interface_name][access_level][return_type]

    def addProperty(self, name, var_type, access, static):
        toAdd = []
        isList = False
        var_type_str = str(var_type)
        if var_type_str.startswith('List<'):
            toAdd = {
                'type': var_type_str.replace('List<','').replace('>',''),
                'properties': []
            }
            isList = True
        if static :
            if 'static' not in self.class_pattern['properties'][access]:
                self.class_pattern['properties'][access]['static'] = {}

            if var_type not in self.class_pattern['properties'][access]['static']:
                self.class_pattern['properties'][access]['static'][var_type] = toAdd

            if not isList:
                self.class_pattern['properties'][access]['static'][var_type].append(name)
            else:
                self.class_pattern['properties'][access]['static'][var_type]['properties'].append(name)
        else:
            if var_type not in self.class_pattern['properties'][access]:
                self.class_pattern['properties'][access][var_type] = []

            self.class_pattern['properties'][access][var_type].append(name)

    def addDynamicProperty(self, name, var_type, access):
        self.addProperty(name, var_type, access, False)

    def addStaticProperty(self, name, var_type, access):
        self.addProperty(name, var_type, access, True)

    def addPublicProperty(self, var_type, name):
        self.addDynamicProperty(name, var_type, 'public')

    def addPublicStaticProperty(self, var_type, name):
        self.addStaticProperty(name, var_type, 'public')

    def addPrivateProperty(self, var_type, name):
        self.addDynamicProperty(name, var_type, 'private')

    def addPrivateStaticProperty(self, var_type, name):
        self.addStaticProperty(name, var_type, 'private')

    def generateCode(self, tab):
        if not tab:
            tab = ''
        c = '\n' + tab
        if not self.access:
            self.access = 'private'
        c += self.access + ' '
        if self.abstract:
            c += 'abstract '
        c += 'class ' + self.name
        p = self.class_pattern

        if 'extends' in p and p['extends']:
            c += ' extends '
            for ext in p['extends']:
                c += ext + ', '
            c = c[:len(c)-2]
        if 'implements' in p and p['implements']:
            c += ' implements '
            for impl in p['implements']:
                c += impl + ', '
            c = c[:len(c)-2]
        
        c += '\n' + tab +'{\n'
        cur_tab = tab + '\t'
        for prop_access,prop_name in p['properties'].items():
            c += self.genPart(p['properties'][prop_access], cur_tab, prop_access)
        # for prop_access,prop_name in p['methods'].items():
        #     c += self.genPart(p['methods'][prop_access], cur_tab, prop_access)
        c += tab + '}\n'
        return c        

    def genPart(self, prop_list, tab, access):
        c = '';
        line_end = ' { get; set; } \n'
        for prop_type, props in prop_list.items():
            if dict == type(props):
                if not str(prop_type).startswith('List<'):
                    prop_keyword = prop_type
                    for prop_type_certain, prop_with_keyword in props.items():
                        d += tab + access + ' ' + prop_keyword + ' ' + prop_type_certain + ' '
                        for prop in prop_with_keyword:
                            c += prop + line_end
                    c += '\n'
                else:
                    for prop_name in props['properties']:
                        d = tab + access + ' ' + prop_type + ' ' + prop_name + line_end
                        c += d
            else:
                for prop_name in props:
                    d = tab + access + ' ' + prop_type + ' ' + prop_name + line_end
                    c += d
        return c