"""
Console script for compas_fea2.
"""
import sys
import os
from pathlib import Path
import click
import compas_fea2
from compas_fea2 import HOME, DATA

import importlib
from cookiecutter.main import cookiecutter
import compas_fea2.model
import inspect
from inspect import getmembers, isfunction, ismodule, isclass

import os
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader


# -------------------------------- MAIN ----------------------------------#
@click.group()
def main():
    """fea2 main.

    Run `fea2 ono-o-one` for more info.
    """
    pass


@main.command()
def one_o_one():
    """Basic explanation of command line usage."""

    click.echo("\nHey there! this is the command line interface (CLI) for compas_fea2!\n")


@main.command()
@click.option('--clean', default='False', help='remove existing directories')
@click.argument('backend', default='abaqus')
def init_backend(backend, clean):
    """Initialize a bare backend module.\n
    backend : txt\n
        The name of the backend. This is used for the
    """
    template_dir = os.path.join(DATA, '_templates')
    base_path = os.path.join(HOME, 'src', 'compas_fea2', 'backends')

    env = Environment(loader=FileSystemLoader(template_dir))
    class_template = env.get_template('class.template')
    import_template = env.get_template('import.template')

    backend_path = os.path.join(base_path, backend)
    os.mkdir(backend_path)

    class_data = {'backend': backend,
                  'backend_cap': backend.capitalize()}
    for module_name in ['model', 'optimisation', 'problem', 'results', 'job']:
        module_path = os.path.join(backend_path, module_name)
        os.mkdir(module_path)
        module = importlib.import_module('compas_fea2.'+module_name)
        sub_module_names = [x[0] for x in getmembers(module, ismodule)]
        for sub_module_name in sub_module_names:
            class_module = '.'.join(['compas_fea2', module_name, sub_module_name])
            class_data['class_module'] = class_module
            sub_module = importlib.import_module(class_module)
            os.chdir(module_path)

            with open(os.path.join(module_path, f'{class_module.split(".")[-1]}.py'), "a") as f:

                imports_data = {'imports': []}
                for fea2_class in getmembers(sub_module, isclass):
                    if fea2_class[1].__module__ == class_module and fea2_class[0][0] != '_':
                        imports_data['imports'].append(f'from {class_module} import {fea2_class[0]}')
                imports_data['imports'] = '\n'.join(imports_data['imports'])
                f.write(import_template.render(imports_data))

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


# -------------------------------- DEBUG ----------------------------------#
if __name__ == "__main__":
    sys.exit(main())
