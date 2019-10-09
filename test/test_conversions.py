import itertools
import numpy as np
import numpy.testing as test

from mass_conversion import conversions as cc
from mass_conversion import utils 

rootfname = 'test/data/test_conversions_{}_to_{}.txt'
m1deflist = ['200m', '200c']
m2deflist = ['200m', '500c']
mdefcombos = itertools.product(m1deflist, m2deflist)


def test_conversions():
    for m1def, m2def in mdefcombos:
        data = np.loadtxt(rootfname.format(m1def, m2def), skiprows=2)
        m1, c1, z, omm, oml, c2true, m2true = np.split(data, 7, axis=1)

        cosmo = {'omega_m': omm, 'omega_k': 1.-omm-oml, 'omega_l':oml}
        c2test = cc.convert_concentration(c1, z, m1def, m2def, cosmo)
        test.assert_allclose(c2test, c2true, rtol=1.e-2)

        delta1, density1 = utils.parse_mdef_string(m1def)
        delta2, density2 = utils.parse_mdef_string(m2def)
        densityratio = utils.compute_density_ratio(density1, density2, z, cosmo)
        m2test = cc._convert_mass(m1, delta2/delta1, densityratio, c2true/c1)
        test.assert_allclose(m2test, m2true, rtol=1.e-8)

