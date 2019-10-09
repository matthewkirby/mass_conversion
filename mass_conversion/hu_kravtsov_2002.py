"""The various fitting functions and formulae from Hu and Kravtsov 2002"""
import numpy as np


def fhalo_ffunc(x):
    r"""Compute f(x), the fitting function that describes the mass enclosed
    within a radius r for an NFW halo.

    From Hu and Kravtsov 2002,

    ..math::
        f(x) = x^3 \left( \ln(1+x^{-1}) - (1+x)^{-1} \right)

    """
    return x*x*x * (np.log(1. + 1./x) - 1./(1. + x))


def inv_fhalo_ffunc(f):
    r"""Use the fitting function from Hu and Kravtsov 2002 for the inverse of
    f(x).

    For an NFW halo, described by a normalization :math:`\rho_s` and a scale
    radius :math:`r_s`, the mass enclosed within a radius r is

    ..math::
        M = 4 \pi \rho_s r^3 f(r_s/r)

        f(x) = x^3 \left( \ln(1+x^{-1}) - (1+x)^{-1} \right)

    Hu and Kravtsov 2002 computed a fitting function :math:`x(f)`

    ..math::
        x(f) = \left[ a_1 f^{2p} + (3/4)^2 \right]^{-1/2} + 2f

        p \equiv a_2 + a_3 \ln f + a_4 (\ln f)^2

    Where :math:`a_1 = 0.5116`, :math:`a_2 = -0.4283`,
    :math:`a_3 = -3.13\times 10^{-3}`, and :math:`a_4 = -3.52\times 10^{-5}`
    """
    a1, a2 = 0.5116, -0.4283
    a3, a4 = -3.13e-3, -3.52e-5
    lnf = np.log(f)
    p = a2 + a3*lnf + a4*lnf*lnf
    return (a1*pow(f, 2.*p) + 0.5625)**(-0.5) + 2.0*f









