import itertools
import numpy as np
import numpy.testing as test

from mass_conversion import conversions as cc
from mass_conversion import utils 
from mass_conversion import cM_models as cm


rootfname = 'test/data/test_conversions_{}_to_{}.txt'
m1deflist = ['200m', '200c']
m2deflist = ['200m', '500c']
mdefcombos = itertools.product(m1deflist, m2deflist)


def load_truth(fname):
    data = np.loadtxt(fname, skiprows=2)
    m1, c1, z, omm, oml, c2true, m2true = np.split(data, 7, axis=1)
    return m1, c1, z, omm, oml, c2true, m2true


def test_conversions():
    """Concentrations to 0.1%, masses to 2%"""
    for m1def, m2def in mdefcombos:
        summary = m1def + ' to ' + m2def
        m1, c1, z, omm, oml, c2true, m2true = load_truth(rootfname.format(m1def, m2def))

        cosmo = {'omega_m': omm, 'omega_k': 1.-omm-oml, 'omega_l':oml}
        c2test = cc.convert_concentration(c1, z, m1def, m2def, cosmo)
        test.assert_allclose(c2test, c2true, rtol=5.e-3, err_msg=summary)

        delta1, density1 = utils.parse_mdef_string(m1def)
        delta2, density2 = utils.parse_mdef_string(m2def)
        densityratio = utils.compute_density_ratio(density1, density2, z, cosmo)
        m2test = cc._convert_mass(m1, delta2/delta1, densityratio, c2true/c1)
        test.assert_allclose(m2test, m2true, rtol=1.e-8)

        m2test_both = cc._convert_mass(m1, delta2/delta1, densityratio, c2test/c1)
        test.assert_allclose(m2test_both, m2true, rtol=2.e-2, err_msg=summary)


def test_fixedc200c():
    """Test the cM model object fixedc200c"""
    m1def, m2def = '200c', '200m'
    m1, c1, z, omm, oml, c2true, m2true = load_truth(rootfname.format(m1def, m2def))
    for i in range(len(m1)):
        model = cm.FixedC200c(c1[i])
        cosmo = {'omega_m': omm[i], 'omega_k': 1.-omm[i]-oml[i], 'omega_l':oml[i]}
        c2test = model(None, z[i], '200m', cosmo=cosmo)
        test.assert_allclose(c2test, c2true[i], rtol=5.e-3)
