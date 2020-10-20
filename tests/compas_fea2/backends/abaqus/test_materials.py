import pytest
import compas_fea2
from compas_fea2.backends.abaqus.model import materials
from compas_fea2.backends.abaqus.model.materials import ElasticIsotropic

young_mod = 1000
poisson_ratio = 0.3
density = 1.0
name = "test"
unilateral = ["nc", "nt", "junk"]

# ==============================================================================
# Tests - Elastic Isotropic
# ==============================================================================


def test_ElasticIsotropic_generate_data_1():
    material_input = ElasticIsotropic(name, young_mod, poisson_ratio, density,
                                      unilateral=unilateral[0])
    function_out = material_input._generate_data()
    expected_out = ("*Material, name={}\n"
                    "*Density\n"
                    "{},\n"
                    "*Elastic\n"
                    "{}, {}\n"
                    "*NO COMPRESSION\n").format(name, density, young_mod, poisson_ratio)
    assert function_out == expected_out


def test_ElasticIsotropic_generate_data_2():
    material_input = ElasticIsotropic(name, young_mod, poisson_ratio, density,
                                      unilateral=unilateral[1])
    function_out = material_input._generate_data()
    expected_out = ("*Material, name={}\n"
                    "*Density\n"
                    "{},\n"
                    "*Elastic\n"
                    "{}, {}\n"
                    "*NO TENSION\n").format(name, density, young_mod, poisson_ratio)
    assert function_out == expected_out


def test_ElasticIsotropic_generate_data_3():
    # FIXME: don't leave this in the future. It's here only to show an example of a badly designed test.
    material_input = ElasticIsotropic(name, young_mod, poisson_ratio, density,
                                      unilateral=unilateral[0])
    function_out = material_input._generate_data()
    expected_out = ("*Material, name={}\n"
                    "*Density\n"
                    "{},\n"
                    "*Elastic\n"
                    "{}, {}\n"
                    "*NO TENSION\n").format(name, density, young_mod, poisson_ratio)
    assert function_out != expected_out


def test_ElasticIsotropic_generate_data_4():
    with pytest.raises(Exception) as exc_info:
        ElasticIsotropic(name, young_mod, poisson_ratio, density, unilateral=unilateral[2])

    assert exc_info.value.args[0] == ("keyword {} for unilateral parameter not recognised. "
                                      "Please review the documentation").format(unilateral[2])
