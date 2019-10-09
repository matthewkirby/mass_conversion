

def parse_mdef_string(mdef):
    """Convert mass definition string to a delta and density definition

    NEED TO DO: Generalize this.
    """
    delta = float(mdef[:-1])
    if 200. < delta < 500.:
        raise ValueError("Mass definition for delta={} outside of\
                          [200, 500] not supported".format(delta))

    if mdef[-1] == 'm':
        density = 'mean'
    elif mdef[-1] == 'c':
        density = 'crit'
    else:
        raise ValueError("Mass definitions only supported with respect to mean or crit density")

    return delta, density


def compute_density_ratio(density1, density2, z, cosmo):
    r"""To convert between mass definitions with respect to the mean and critical
    density, you need :math:`\Omega_M`. This function computes the ratio and raises
    an exception if :mean:`\Omega_M` was not specified if it was required.
    
    This is a separate function so that I can keep these ugly if statements and
    checks out of the functions doing the science.
    
    Parameters
    ----------
    density1 : str ('mean', 'crit')
        Density definition of the input quantity
    density2 : str ('mean', 'crit')
        Density definition of the output quantity
    z: float
        Redshift of the halo
    cosmo: dict
        Contains cosmology parameters, Omega_M, Omega_K, Omega_L to convert between mass
        definitions with respect to the mean and critical density

    Returns
    -------
    rho2_over_rho1 : float
        The ratio of the densities, density2/density1
    """
    densityratio = density2 + '/' + density1
    # If the density definitions are the same, don't need OmegaM
    if densityratio in ['mean/mean', 'crit/crit']:
        return 1.0

    # However, if we need to change between them, check that we have a value
    if cosmo is None:
        raise ValueError("OmegaM required to convert between rho_c and rho_m mass defs")

    # Compute the density ratio
    if densityratio == 'crit/mean':
        return ez_sq(z, cosmo)/(cosmo['omega_m']*(1.0+z)**3)
    elif densityratio == 'mean/crit':
        return cosmo['omega_m']*(1.0+z)**3/ez_sq(z, cosmo)
    else:
        raise ValueError("densityratio: {} not recognized!!".format(densityratio))


def ez_sq(z, cosmo):
    """The LCDM dimensionless Hubble parameter squared"""
    opz = 1.0 + z
    return cosmo['omega_m']*opz**3 + cosmo['omega_k']*opz**2 + cosmo['omega_l']






