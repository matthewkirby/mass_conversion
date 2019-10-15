import numpy as np
import mass_conversion.hu_kravtsov_2002 as hu02
import mass_conversion.utils as utils
import mass_conversion.cM_models as models



def select_cM_relation(cMstring):
    """Parse the c-M relation string into a callable

    Currently supported: fixedc200c
    
    Parameters
    ----------
    cMstring: str
        The name of the cM relation to use
        
    Returns
    -------
    cMcallable: callable
        An instance of a child of `ConcentrationModel`
    """
    if cMstring.lower() == 'fixedc200c':
        cMcallable = models.FixedC200c
    else:
        raise ValueError("{} is not a supported c-M relation.".format(cMstring))
    return cMcallable


def convert_concentration(c1, z, m1def, m2def, cosmo=None):
    r"""Convert concentration in a given mass definition to a different mass definition

    :math:`\Omega_M` is only required if converting between mass definitions in terms of
    the critical and mean densities.

    Parameters
    ----------
    c1 : float
        Input concentration in m1def
    z: float
        Redshift of the halo
    m1def : str
        Mass definition of the input concentration
    m2def : str
        Mass definition of the output concentration
    cosmo: dict, optional
        Contains cosmology parameters, Omega_M, Omega_K, Omega_L to convert between mass
        definitions with respect to the mean and critical density

    Returns
    -------
    c2 : float
        Concentration in m2def
    """
    delta1, density1 = utils.parse_mdef_string(m1def)
    delta2, density2 = utils.parse_mdef_string(m2def)
    rho2_over_rho1 = utils.compute_density_ratio(density1, density2, z, cosmo)

    arg = (delta2/delta1)*rho2_over_rho1
    inv_c2 = hu02.inv_fhalo_ffunc(arg*hu02.fhalo_ffunc(1.0/c1))

    return 1./inv_c2


def _convert_mass(m1, deltaratio, densityratio, cratio):
    """Convert an input mass from m1def to m2def given the concentrations

    This function is intended to be internal and is only separate for testing purposes.
    """
    return m1 * densityratio * deltaratio * cratio**3


def convert_m1_to_m2(m1, z, m1def, m2def, cMrelation, cosmo=None):
    """Given spherical overdensity mass, redshift, and a concentration-Mass relation,
    compute halo mass in a different spherical overdensity definition assuming a fixed
    NFW profile.

    Parameters
    ----------
    m1: float
        Input mass in m1def
    z: float
        Redshift of the halo(s)
    m1def : str
        Input  mass definition
    m2def : str
        Output mass definition
    cMrelation: callable
        Concentration-Mass relation to use to convert the masses
    cosmo: dict, optional
        Contains cosmology parameters, Omega_M, Omega_K, Omega_L to convert between mass
        definitions with respect to the mean and critical density
        
    Returns
    -------
    m2: float
        Output mass in m2def
    """
    c1 = cMrelation(m1, z, m1def, cosmo)
    delta1, density1 = utils.parse_mdef_string(m1def)
    delta2, density2 = utils.parse_mdef_string(m2def)

    rho2_over_rho1 = utils.compute_density_ratio(density1, density2, z, cosmo)
    c2 = convert_concentration(c1, z, m1def, m2def, cosmo)
    m2 = _convert_mass(m1, delta2/delta1, rho2_over_rho1, c2/c1)

    return m2
    

def main():
    cosmo = {'omega_m': 0.3, 'omega_k': 0.0, 'omega_l': 0.7}
    z = 0.5
    m1 = 1.e15
    m1def, m2def = '200c', '200m'
    cMrelation = models.FixedC200c(4.)
    m2 = convert_m1_to_m2(m1, z, m1def, m2def, cMrelation, cosmo)

    print("{:e}".format(m2))
    print("{:e}".format(1193597274349967.2))




if __name__ == "__main__":
    main()






