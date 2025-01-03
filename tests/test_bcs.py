from compas_fea2.model.bcs import FixedBC, PinnedBC, RollerBCX

def test_fixed_bc():
    bc = FixedBC()
    assert bc.x
    assert bc.y
    assert bc.z
    assert bc.xx
    assert bc.yy
    assert bc.zz

def test_pinned_bc():
    bc = PinnedBC()
    assert bc.x
    assert bc.y
    assert bc.z
    assert not bc.xx
    assert not bc.yy
    assert not bc.zz

def test_roller_bc_x():
    bc = RollerBCX()
    assert not bc.x
    assert bc.y
    assert bc.z
    assert not bc.xx
    assert not bc.yy
    assert not bc.zz
