from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from abaqus import *
    from abaqusConstants import *
except:
    pass

import sys

from compas_fea2.backends.abaqus.writer import Writer

from compas_fea2.backends.abaqus.job import launch_job
from compas_fea2.backends.abaqus.job  import odb_extract

from subprocess import Popen
from subprocess import PIPE

from time import time

import json
import os


# Author(s): Andrew Liew (github.com/andrewliew)


__all__ = [
    'input_generate',
    'launch_process',
]


node_fields    = ['rf', 'rm', 'u', 'ur', 'cf', 'cm']
element_fields = ['sf', 'sm', 'sk', 'se', 's', 'e', 'pe', 'rbfor', 'ctf']


def input_generate(structure, fields, output):

    """ Creates the Abaqus .inp file from the Structure object.

    Parameters
    ----------
    structure : obj
        The Structure object to read from.
    fields : list
        Data field requests.
    output : bool
        Print terminal output.

    Returns
    -------
    None

    """

    filename = '{0}{1}.inp'.format(structure.path, structure.name)

    if isinstance(fields, str):
        fields = [fields]

    if 'u' not in fields:
        fields.append('u')

    with Writer(structure=structure, filename=filename, fields=fields) as writer:

        writer.write_heading()
        writer.write_nodes()
        writer.write_node_sets()
        writer.write_boundary_conditions()
        writer.write_materials()
        writer.write_elements()
        writer.write_element_sets()
        writer.write_steps()

    if output:
        print('***** Abaqus input file generated: {0} *****\n'.format(filename))


def launch_process(structure, exe, cpus, output):

    """ Runs the analysis through Abaqus.

    Parameters
    ----------
    structure : obj
        Structure object.
    exe : str
        Abaqus exe path to bypass defaults.
    cpus : int
        Number of CPU cores to use.
    output : bool
        Print terminal output.

    Returns
    -------
    None

    """

    name = structure.name
    path = structure.path
    temp = '{0}{1}/'.format(path, name)

    # Analyse

    tic = time()

    subprocess = 'noGUI={0}'.format(launch_job.__file__.replace('\\', '/'))
    success    = False

    if not exe:

        args = ['abaqus', 'cae', subprocess, '--', str(cpus), path, name]
        p    = Popen(args, stdout=PIPE, stderr=PIPE, cwd=temp, shell=True)

        while True:

            line = p.stdout.readline()
            if not line:
                break
            line = str(line.strip())

            if output:
                print(line)

            if 'COMPLETED' in line:
                success = True

        stdout, stderr = p.communicate()

        if output:
            print(stdout)
            print(stderr)

    else:

        os.chdir(temp)
        os.system('{0} {1} -- {2} {3} {4}'.format(exe, subprocess, cpus, path, name))

        success = True

    toc = time() - tic

    if not success:

        try:

            with open(temp + name + '.sta', 'r') as f:

                if 'COMPLETED SUCCESSFULLY' in f.readlines()[-1]:
                    success = True

        except:
            pass

    if success:

        if output:
            print('***** Analysis successful - analysis time : {0} s *****'.format(toc))

    else:
        print('***** Analysis failed *****')



