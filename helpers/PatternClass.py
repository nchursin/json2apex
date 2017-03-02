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
#     "extends": [],
#     "implements": [
#         "Comparable",
#         "Schedulable"
#     ],
#     "properties":
#     {
#         "public":
#         {
#             "someStaticVar": {
#                 "type" : "Integer",
#                 "static" : true
#             },
#             "someVar": {
#                 "type" : "String"
#             }
#         },
#         "private":
#         {
#             "somePrivateStaticVar": {
#                 "type" : "Integer",
#                 "static" : true
#             },
#             "somePrivateVar": {
#                 "type" : "String"
#             }
#         }
#     },
#     "methods":
#     {
#         "public":
#         {
#             "void":
#             [
#                 {
#                     "name": "methodName",
#                     "static": false,
#                     "arguments":
#                     {
#                         "number": "Integer",
#                         "str": "String"
#                     }
#                 }
#             ]
#         }
#     }
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

    def __init__(self, name, access='private', abstract=False, virtual=False):
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
        self.virtual = virtual

    @classmethod
    def fromSchema(cls, name, schema):
        obj = cls(name, 'public')
        obj.class_pattern = schema
        return obj

    def toJson(self):
        return json.dumps(self.class_pattern)

    def addExtends(self, class_name):
        self.class_pattern['extends'].append(class_name)

    def addInterface(self, interface_name):
        self.class_pattern['implements'].append(interface_name)

    def addProperty(self, name, var_type, access, static):
        var_object = {}
        var_object['type'] = var_type
        var_object['static'] = static
        self.class_pattern['properties'][access][name] = var_object

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

    def loadInterfaces(self):
        for interface_name in self.class_pattern['implements']:
            interface_pattern = loadInterfacePattern(interface_name)
            if interface_pattern != None:
                for access_level, methods in interface_pattern['methods'].items():
                    self.class_pattern['methods'][access_level].update(methods)

    def generateCode(self, tab = ''):
        class_template = Template('other/SimpleClassTemplate')
        class_template.addVar('intends', tab)
        class_template.addVar('access', self.access)
        class_type = ''
        if self.virtual:
            class_type = 'virtual'
        elif self.abstract:
            class_type = 'abstract'
        class_template.addVar('classType', class_type)
        class_template.addVar('className', self.name)
        p = self.class_pattern

        if 'extends' not in p:
            p['extends'] = []
        if 'implements' not in p:
            p['implements'] = []
        class_template.addVar('extends', ', '.join(p['extends']))
        class_template.addVar('implements', ', '.join(p['implements']))
        self.loadInterfaces()
        
        prop_list = []
        for prop_access,props in p['properties'].items():
            for prop_name, prop_desc in props.items():
                prop_def = self.genPropertyCode(prop_access, prop_name, prop_desc)
                prop_list.append( prop_def )
        methods_code = []
        for method_access, methods in p['methods'].items():
            for method_name, method_desc in methods.items():
                method_code = self.genMethodCode(method_access, method_name, method_desc)
                method_code = tab + '\t' + method_code.replace('\n', '\n\t' + tab)
                methods_code.append(method_code)
        class_template.addVar('properties', prop_list)
        class_template.addVar('methods', '\n'.join(methods_code))
        result = class_template.compile()
        del class_template
        return result

    def genMethodCode(self, method_access, method_name, method_desc):
        t = Template('other/Method')
        t.addVar('access', method_access)
        t.addVar('methodName', method_name)
        if 'static' in method_desc:
            t.addVar('static', method_desc['static'])
        else:
            t.addVar('static', False)

        if 'returns' in method_desc:
            t.addVar('returnType', method_desc['returns'])
        else:
            t.addVar('returnType', 'void')

        arg_str = ''
        if 'arguments' in method_desc:
            for arg_name, arg_type in method_desc['arguments'].items():
                arg_str += arg_type + ' ' + arg_name + ', '
            if arg_str:
                arg_str = arg_str[:len(arg_str)-2]
        t.addVar('methodArguments', arg_str)

        if 'comment' in method_desc:
            t.addVar('comment', method_desc['comment'])
        else:
            t.addVar('comment', '')

        if 'todo_comment' in method_desc:
            t.addVar('todo_comment', method_desc['todo_comment'])
        else:
            t.addVar('todo_comment', '')

        result = t.compile()
        del t
        return result

    def genPropertyCode(self, access, prop_name, prop_desc):
        t = Template('other/ClassProperty')
        t.addVar('createGetSet', True)
        t.addVar('access', access)
        t.addVar('propName', prop_name)
        if 'static' not in prop_desc:
            prop_desc['static'] = False
        t.addVar('static', prop_desc['static'])
        t.addVar('valueType', prop_desc['type'])
        return t.compile()