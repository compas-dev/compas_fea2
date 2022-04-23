import importlib
from cookiecutter.main import cookiecutter
import compas_fea2.model
import inspect
from inspect import getmembers, isfunction, ismodule, isclass

import os
from jinja2 import Template

import_template = Template(
    """from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

{{ imports }}
    """
)

class_template = Template("""
class {{ backend_cap }}{{ class_name }}({{ class_name }}):
    \"\"\" {{ backend_cap }} implementation of :class:`{{ class_module }}.{{ class_name }}`.\n
    \"\"\"
    __doc__ += {{ class_name }}.__doc__

    def __init__{{ class_parameters }}:
        super({{ backend_cap }}{{ class_name }}, self).__init__({{ base_class_parameters }})
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

""")

class_data = {
    'backend_cap': 'Ansys',
    'class_name': 'FIxBC',
    'class_module': 'compas_fea2.module.bcs',
    'class_parameters': 'nodes, *args, **kwargs'
}

imports_data = {
    'imports': []
}

backend = 'ansys'

base_path = compas_fea2.TEMP
backend_path = os.path.join(base_path, backend)
os.mkdir(backend_path)
for module_name in ['model']:  # , 'optimisation', 'problem', 'results', 'job']:
    module_path = os.path.join(backend_path, module_name)
    os.mkdir(module_path)
    module = importlib.import_module('compas_fea2.'+module_name)
    sub_module_names = [x[0] for x in getmembers(module, ismodule)]
    for sub_module_name in sub_module_names:
        class_module = '.'.join(['compas_fea2', module_name, sub_module_name])
        class_data['class_module'] = class_module
        sub_module = importlib.import_module(class_module)
        os.chdir(module_path)
        with open(os.path.join(module_path, f'{class_module}.py'), "a") as f:

            for fea2_class in getmembers(sub_module, isclass):
                if fea2_class[1].__module__ == class_module and fea2_class[0][0] != '_':
                    imports_data['imports'].append(f'from {class_module} import {fea2_class[0]}')
            imports_data['imports'] = '\n'.join(imports_data['imports'])
            f.write(import_template.render(imports_data))
            imports_data['imports'] = []

            for fea2_class in getmembers(sub_module, isclass):
                if fea2_class[1].__module__ == class_module and fea2_class[0][0] != '_':
                    class_data['class_name'] = fea2_class[0]
                    class_data['class_parameters'] = str(inspect.signature(fea2_class[1].__init__))
                    params = []
                    for par in inspect.signature(fea2_class[1].__init__).parameters.values():
                        if par.name not in ['self', 'args', 'kwargs']:
                            params.append(par.name+'='+par.name)
                        elif par.name == 'args':
                            params.append('*args')
                        elif par.name == 'kwargs':
                            params.append('**kwargs')
                    class_data['base_class_parameters'] = ', '.join(params)
                    f.write(class_template.render(class_data))
