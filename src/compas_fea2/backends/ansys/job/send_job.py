from compas_fea2.backends.ansys.writer import write_static_analysis_request
from compas_fea2.backends.ansys.writer import write_modal_analysis_request
from compas_fea2.backends.ansys.writer import write_harmonic_analysis_request
from compas_fea2.backends.ansys.writer import write_acoustic_analysis_request

# Author(s): Tomas Mendez Echenagucia (github.com/tmsmendez)


__all__ = [
    'input_generate',
    'make_command_file_static',
    'make_command_file_modal',
    'make_command_file_harmonic',
]


def input_generate(structure):
    """ Generates Ansys input file.

    Parameters:
        structure (obj): Structure object.

    Returns:
        None
    """
    name = structure.name
    path = structure.path
    stypes = [structure.steps[skey].type for skey in structure.steps]

    if 'static' in stypes:
        make_command_file_static(structure, path, name)
    elif 'modal' in stypes:
        make_command_file_modal(structure, path, name)
    elif 'harmonic' in stypes:
        make_command_file_harmonic(structure, path, name, skey)
    elif 'acoustic' in stypes:
        make_command_file_acoustic(structure, path, name, skey)
    else:
        raise ValueError('This analysis type has not yet been implemented for Compas Ansys')


def make_command_file_static(structure, path, name):
    """ Generates Ansys input file for static analysis.

    Parameters:
        structure (obj): Structure object.

    Returns:
        None
    """
    write_static_analysis_request(structure, path, name)


def make_command_file_modal(structure, path, name):
    """ Generates Ansys input file for modal analysis.

    Parameters:
        structure (obj): Structure object.

    Returns:
        None
    """
    write_modal_analysis_request(structure, path, name)


def make_command_file_harmonic(structure, output_path, filename, skey):
    """ Generates Ansys input file for harmonic analysis.

    Parameters:
        structure (obj): Structure object.

    Returns:
        None
    """
    write_harmonic_analysis_request(structure, output_path, filename, skey)


def make_command_file_acoustic(structure, output_path, filename, skey):
    """ Generates Ansys input file for acoustic analysis.

    Parameters:
        structure (obj): Structure object.

    Returns:
        None
    """
    write_acoustic_analysis_request(structure, output_path, filename, skey)



