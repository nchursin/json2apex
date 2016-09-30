import os
import json

# {
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
#               {
#                   'name': 'methodName',
#                   'arguments':
#                   {
#                       'String': [],
#                       'Integer': []
#                   }
#               }
#           }
#       }
#   }
# }

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

class Pattern:
    class_pattern = {}
    name = ''
    access = ''
    abstract = ''

    generated_code = ''

    def __init__(self, name, access, abstract):
        self.class_pattern = {
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
        c += 'class ' + self.name + '\n' + tab +'{\n'
        cur_tab = tab + '\t'
        p = self.class_pattern
        for prop_access,prop_name in p['properties'].items():
            c += self.genPart(p['properties'][prop_access], cur_tab, prop_access)
        for prop_access,prop_name in p['methods'].items():
            c += self.genPart(p['methods'][prop_access], cur_tab, prop_access)
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