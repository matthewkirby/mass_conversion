

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


def compute_density_ratio(density1, density2, omega_m):
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
    omega_m : float
        The local matter density of the universe in units of the critical density

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
    if omega_m is None:
        raise ValueError("OmegaM required to convert between rho_c and rho_m mass defs")

    # Compute the density ratio
    if densityratio is 'crit/mean':
        return 1.0/omega_m
    elif densityratio is 'mean/crit':
        return omega_m
    else:
        raise ValueError("densityratio={} not recognized!!".format(densityratio))









