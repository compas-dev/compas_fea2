from struct import pack
import sys
import os
import shutil
from turtle import back
import click
import compas_fea2
from compas_fea2 import HOME, DATA

import importlib
import compas_fea2.model
import inspect
from inspect import getmembers, isfunction, ismodule, isclass

import os
from jinja2 import Environment, FileSystemLoader

# from compas_fea2.utilities._cookiecutter import COOKIECUTTER_TEMPLATES


def scan_package(package, ignore_protected=True):
    """Scan a package and return its structure.

    Parameters
    ----------
    package : :class:`module`
        The package to be scanned.
    ignore_protected : bool, optional
        Ignore protected members (those starting with '_'), by default True.

    Returns
    -------
    _type_
        _description_
    """
    package_data = {
        'module': package,
    }
    try:
        base_path = package.__path__[0]
    except:
        base_path = None
    if base_path:
        for p in os.listdir(base_path):
            if os.path.isdir(os.path.join(base_path, p)):
                if ignore_protected and p[0] == '_':
                    continue
                package_data.setdefault('sub_packages', {})[p] = scan_package(
                    importlib.import_module('.'.join([package.__name__, p])))

    for m in getmembers(package, ismodule):
        if ignore_protected and m[0][0] == '_':
            continue
        if m[1].__package__ == package.__name__:
            package_data.setdefault('sub_modules', {})[m[0]] = scan_package(m[1])

    for c in getmembers(package, isclass):
        if ignore_protected and c[0][0] == '_':
            continue
        if c[1].__module__ == package.__name__:
            package_data.setdefault('classes', []).append(c)

    return package_data


def mirror_package(path, package_data, **kwargs):
    # path = os.path.join(path, package_data['module'].__name__.split(".")[-1])
    if not os.path.exists(path):
        os.mkdir(path)
    if 'sub_packages' in package_data:
        for sub_package, sub_package_data in package_data['sub_packages'].items():
            sub_package_path = os.path.join(path, sub_package_data['module'].__name__.split(".")[-1])
            mirror_package(path=sub_package_path, package_data=sub_package_data, backend=kwargs['backend'])

    if 'sub_modules' in package_data:
        # path = os.path.join(path, package_data['module'].__name__.split(".")[-1])

        init_modules(package_data, kwargs['backend'], path)

    if 'classes' in package_data:
        init_classes(package_data, kwargs['backend'], path)


def init_modules(module_data, backend, path):
    # module_path = os.path.join(path, module_data['module'].__name__.split(".")[-1])
    module_path = path
    # if not os.path.exists(module_path):
    #     os.mkdir(module_path)
    for sub_module, sub_module_data in module_data['sub_modules'].items():
        mirror_package(path=module_path, package_data=sub_module_data, backend=backend)


def init_classes(classes_data, backend, path):

    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '_templates')))
    class_template = env.get_template('class.template')
    import_template = env.get_template('import.template')

    class_module = classes_data["module"].__name__
    class_module_name = class_module.split(".")[-1]
    # if not os.path.exists(path):
    #     os.mkdir(path)
    imports_data = {}
    with open(os.path.join(path, f'{class_module_name}.py'), "a") as f:
        for c in classes_data['classes']:
            imports_data.setdefault('imports', []).append(f'from {class_module} import {c[0]}')
        imports_data['imports'] = '\n'.join(imports_data['imports'])
        f.write(import_template.render(imports_data))
        imports_data = {}

    class_data = {'backend': backend,
                  'backend_cap': backend.capitalize()
                  }
    with open(os.path.join(path, f'{class_module_name}.py'), "a") as f:
        for c in classes_data['classes']:
            class_data['class_name'] = c[0]
            class_data['class_parameters'] = str(inspect.signature(c[1].__init__))

            params = []
            for par in inspect.signature(c[1].__init__).parameters.values():
                if par.name not in ['self', 'args', 'kwargs']:
                    params.append(par.name+'='+par.name)
                elif par.name == 'args':
                    params.append('*args')
                elif par.name == 'kwargs':
                    params.append('**kwargs')
            class_data['base_class_parameters'] = ', '.join(params)

            f.write(class_template.render(class_data))


if __name__ == '__main__':
    import compas_fea2.problem
    import compas_fea2
    from pprint import pprint

    classes_data = scan_package(compas_fea2.problem, ignore_protected=True)
    pprint(classes_data)

    backend = 'ansys'
    clean = True

    path = os.path.join(compas_fea2.TEMP, backend)
    if clean and os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    mirror_package(path=path, package_data=classes_data, backend='abaqus')
