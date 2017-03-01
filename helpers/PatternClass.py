import os, os.path
import json
from TemplateHelper import Template
from TemplateHelper import TemplateArgs
# import sublime, sublime_plugin

def loadPattern(pattern_name):
    pattern_ext = '.json'
    pattern_dir = 'patterns/'
    pattern_path = pattern_dir + pattern_name + pattern_ext
    if os.path.isfile(pattern_path):
        with open(pattern_path) as f:
            content = f.read()
        return json.loads(content)
    else:
        return None

def loadInterfacePattern(interface_name):
    interface_dir = 'interface/'
    return loadPattern(interface_dir + interface_name)

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
#          'void':
#          [
#              'name': 'methodName',
#              'static': False,
#              'arguments':
#              {
#                  'number': 'Integer',
#                  'str': 'String'
#              }
#          ]
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
        self.addInterface('Comparable')
        self.addInterface('SchedulableContext')

    def toJson(self):
        return json.dumps(self.class_pattern)

    def addExtends(self, class_name):
        self.class_pattern['extends'].append(class_name)

    def addInterface(self, interface_name):
        self.class_pattern['implements'].append(interface_name)
        interface_pattern = loadInterfacePattern(interface_name)
        if interface_pattern != None:
            for access_level in interface_pattern['methods']:
                for return_type in interface_pattern['methods'][access_level]:
                    if return_type not in self.class_pattern['methods'][access_level]:
                        self.class_pattern['methods'][access_level][return_type] = []
                    self.class_pattern['methods'][access_level][return_type] += interface_pattern['methods'][access_level][return_type]

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
        methods_code = []
        for method_access, method_ret_types in p['methods'].items():
            args = TemplateArgs()
            args.addVar('access', method_access)
            for ret_type, methods_list in method_ret_types.items():
                args.addVar('returnType', ret_type)
                for method in methods_list:
                    if 'static' in method and method['static']:
                        args.addVar('static', 'static')
                    else:
                        args.addVar('static', '')
                    args.addVar('methodName', method['name'])
                    arg_str = ''
                    if 'arguments' in method:
                        for arg_name, arg_type in method['arguments'].items():
                            arg_str += arg_type + ' ' + arg_name + ', '
                        if arg_str:
                            arg_str = arg_str[:len(arg_str)-2]
                    args.addVar('methodArguments', arg_str)
                    if 'todo_comment' in method and method['todo_comment']:
                        args.addVar('todo_comment', method['todo_comment'])
                    else:
                        args.addVar('todo_comment', '')
                    t = Template('other/Method')
                    t.addArgs(args)
                    method_code = t.compile()
                    method_code = tab + '\t' + method_code.replace('\n', '\n\t' + tab)
                    methods_code.append(method_code)
        c += '\n'
        c += '\n'.join(methods_code)
        c += '\n' + tab + '}\n'
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