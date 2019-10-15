from cosmosis.datablock import option_section
import cM_models as models
import conversions as conv


supported_cM_models = ['fixedc200c']


def setup(options):
    # Load the cM model specified in the config file and ensure that it is supported
    cM_model_id = options[option_section, "cM_model"]
    if cM_model_id not in supported_cM_models:
        raise ValueError("{}, is not a supported c-M relation.".format(cM_model_id))

    # Initialize the model
    if cM_model_id is 'fixedc':
        fixedc = options.get_float(option_section, "c200c")
        cMmodel = models.FixedC200c(fixedc)

    return cMmodel


def execute(block, config):
    # Rename the input for clarity
    cMmodel = config

    # Load the cosmology from the chain
    omega_m = block["cosmological_parameters", "omega_M"]
    omega_k = block["cosmological_parameters", "omega_k"]
    omega_l = block["cosmological_parameters", "omega_l"]
    omega_nu = block["cosmological_parameters", "omega_nu"]

    # This is only used for rho_c(z) = rho_c*H^2(z) so we keep the neutrino contribution.
    cosmo = {'omega_m': omega_m, 'omega_k': omega_k, 'omega_l': omega_l}

    # Load the masses used for the mass function and convert to M200m
    # after subtracting off the neutrino component
    mass_200m = block["mass_function", "m_h"] * (omega_m - omega_nu)
    zlist = block["mass_function", "z"]

    # For each mass, convert to M500c
    mass_500c = np.array([conv.convert_m1_to_m2(mass_200m, z, '200m', '500c', cMmodel, cosmo=cosmo)
                          for z in zlist])

    # Save it to the data block
    outname = "where_is_this"
    block[outname, "m200m"] = mass_200m
    block[outname, "z"] = zlist
    block[outname, "m500c"] = mass_500c

    # Return 0 if gucci
    return 0


def cleanup(config):
    pass
