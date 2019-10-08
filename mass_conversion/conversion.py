import numpy as np
import utils



def select_cM_relation(cMstring):
    """Parse the c-M relation from the ini file into a callable."""
    if cMstring.lower() == 'child18':
        cMcallable = concentration_child18
    else:
        raise ValueError("{} is not a supported c-M relation.".format(cMstring))
    return cMcallable


# def fhalo_ffunc(x):
#     r"""Compute f(x), the fitting function that describes the mass enclosed
#     within a radius r for an NFW halo.
#     
#     From Hu and Kravtsov 2002, 
#
#     ..math::
#         f(x) = x^3 \left( \ln(1+x^{-1}) - (1+x)^{-1} \right)
#
#     """
#     return x*x*x * (np.log(1. + 1./x) - 1./(1. + x))


# def inv_fhalo_ffunc(f):
#     r"""Use the fitting function from Hu and Kravtsov 2002 for the inverse of
#     f(x).
#
#     For an NFW halo, described by a normalization :math:`\rho_s` and a scale
#     radius :math:`r_s`, the mass enclosed within a radius r is
#
#     ..math::
#         M = 4 \pi \rho_s r^3 f(r_s/r)
#
#         f(x) = x^3 \left( \ln(1+x^{-1}) - (1+x)^{-1} \right)
#
#     Hu and Kravtsov 2002 computed a fitting function :math:`x(f)`
#
#     ..math::
#         x(f) = \left[ a_1 f^{2p} + (3/4)^2 \right]^{-1/2} + 2f
#
#         p \equiv a_2 + a_3 \ln f + a_4 (\ln f)^2
#
#     Where :math:`a_1 = 0.5116`, :math:`a_2 = -0.4283`,
#     :math:`a_3 = -3.13\times 10^{-3}`, and :math:`a_4 = -3.52\times 10^{-5}`
#     """
#     a1, a2 = 0.5116, -0.4283
#     a3, a4 = -3.13e-3, -3.52e-5
#     lnf = np.log(f)
#     p = a2 + a3*lnf + a4*lnf*lnf
#     return (a1*pow(f, 2.*p) + 0.5625)**(-0.5) + 2.0*f


# def parse_mdef_string(mdef):
#     """Convert mass definition string to a delta and density definition
#
#     NEED TO DO: Generalize this.
#     """
#     delta = float(mdef[:-1])
#     if 200. < delta < 500.:
#         raise ValueError("Mass definition for delta={} outside of\
#                           [200, 500] not supported".format(delta))
#
#     if mdef[-1] == 'm':
#         density = 'mean'
#     elif mdef[-1] == 'c':
#         density = 'crit'
#     else:
#         raise ValueError("Mass definitions only supported with respect to mean or crit density")
#     
#     return delta, density


def convert_m1_to_m2(m1, m1def, m2def, omega_m, cMrelation):
    """Currently only supports m1=m200m and m2=m500c"""
    c1 = cMrelation('test')
    delta1, density1 = utils.parse_mdef_string(m1def)
    delta2, density2 = utils.parse_mdef_string(m2def)

    if density1 == density2:
        densratio = 1.0
    elif density1 == 'mean':
        densratio = 1.0/omega_m
    elif density1 == 'crit':
        densratio = omega_m

    invf_arg = densratio * (delta2/delta1) * fhalo_ffunc(1.0/c1)
    c2 = 1./inv_fhalo_ffunc(invf_arg)
    m2 = m1 * densratio * (delta2/delta1) * (c2/c1)**3

    return m2
    

def main():
    omega_m = 0.3
    m1 = 1.e14
    m1def, m2def = '200m', '500c'

    cMrelation = select_cM_relation('Child18')
    m2 = convert_m1_to_m2(m1, m1def, m2def, omega_m, cMrelation)

    print('{}: {:e}'.format(m1def, m1))
    print('{}: {:e}'.format(m2def, m2))




if __name__ == "__main__":
    main()






