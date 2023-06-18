import pytest
import compas_fea2

from compas_fea2.model import Concrete

from compas_fea2.model.materials import Concrete, ElasticIsotropic, Stiff, UserMaterial

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
    function_out = material_input._generate_jobdata()
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
    function_out = material_input._generate_jobdata()
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
    function_out = material_input._generate_jobdata()
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


# ==============================================================================
# Tests - Stiff
# ==============================================================================

def test_Stiff_generate_data():
    # Get the default values for p and v
    init_stiff = Stiff("def", 100)
    # My material
    material_input = Stiff(name, young_mod)
    function_out = material_input._generate_jobdata()
    expected_out = ("*Material, name={}\n"
                    "*Density\n"
                    "{},\n"
                    "*Elastic\n"
                    "{}, {}\n").format(name, init_stiff.p, young_mod, init_stiff.v['v'])
    assert function_out == expected_out


# ==============================================================================
# Tests - Steel
# ==============================================================================

def test_Steel_generate_data():
    E = 1000.0
    fy = 400.0
    fu = 500.0
    eu = 30.0
    # Done in Steel constructor
    ep = eu * 1E-2 - (fy * 1E6) / (E * 1E9)
    # My material
    material_input = Steel("steely", fy, fu, eu, E, 0.3, 1.0)
    function_out = material_input._generate_jobdata()
    # Expected
    # Materials are units dependent - (E, f<y,u>)
    expected_out = ("*Material, name={}\n"
                    "*Density\n"
                    "{},\n"
                    "*Elastic\n"
                    "{}, {}\n"
                    "*Plastic\n"
                    "{}, {}\n"
                    "{}, {}").format("steely", 1.0, E*1E9, 0.3, fy*1E6, 0, fu*1E6, ep)
    assert function_out == expected_out


# ==============================================================================
# Tests - Concrete
# ==============================================================================

def test_Concrete_generate_data():
    # name = "concrety"
    # fck = 1000.0
    # v = poisson_ratio
    # p = 1.0
    # fr = [2.5, 1.0]
    # material_base = Concrete(name, fck, v, p, fr)
    # # My material
    # material_input = Concrete(name, fck, v, p, fr)
    # function_out = material_input._generate_jobdata()
    # print(function_out)
    # # Expected
    # # Materials are units dependent - (E, f<y,u>)
    # TODO: to complicated to test yet
    pass

# ==============================================================================
# Tests - UserMaterial
# ==============================================================================


def test_UserMaterial_constructor_1():
    """ Without any constants """
    name = 'user'
    sub_path = '/user/project/my_material'
    p = 2.0
    material_input = UserMaterial('user', sub_path, p)

    assert material_input.get_constants() == [[], material_input.data]


def test_UserMaterial_constructor_2():
    """
    Without a few constants.
    """
    name = 'user'
    sub_path = '/user/project/my_material'
    p = 2.0
    extra_args = dict(t=100,
                      a="xyz",
                      c=-30.5,
                      key=1)
    material_input = UserMaterial('user', sub_path, p, **extra_args)

    # Test _generate_jobdata()

    expected_res = '*Material, name={}\n*Density\n{},'\
                   '\n*User Material, constants={}\n{}, xyz, {}'.format(name, p,
                                                                        len(extra_args),
                                                                        extra_args['key'],
                                                                        extra_args['c'],
                                                                        extra_args['a'],
                                                                        extra_args['t'])

    # Test get_constants()

    expected_res = [*extra_args.values(), [*extra_args.values()], material_input.jobdata]
    assert material_input.get_constants() == expected_res
