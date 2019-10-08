from cosmosis.datablock import names, option_section


# We have a collection of commonly used pre-defined block section names.
# If none of the names here is relevant for your calculation you can use any
# string you want instead.
####################################################################################
# cosmo = names.cosmological_parameters
supported_cM_models = ['fixedc']


def setup(options):
    # Load the cM model specified in the config file
    universal_cM_model = options[option_section, "cM_model"]
    if universal_cM_model not in supported_cM_models:
        raise ValueError("{}, is not a supported c-M relation.".format(universal_cM_model))

    if cM_model is 'fixedc':


    #The call above will crash if "mode" is not found in the ini file.
    #Sometimes you want a default if nothing is found:
    high_accuracy = options.get(option_section, "high_accuracy", default=False)

    #Now you have the input options you can do any useful preparation
    #you want.  Maybe load some data, or do a one-off calculation.
    loaded_data = my_calculation.prepare_something(mode)

    #Whatever you return here will be saved by the system and the function below
    #will get it back.  You could return 0 if you won't need anything.
    return loaded_data


def execute(block, config):
    #This function is called every time you have a new sample of cosmological and other parameters.
    #It is the main workhorse of the code. The block contains the parameters and results of any 
    #earlier modules, and the config is what setup returned

    # Just a simple rename for clarity.
    loaded_data = config

    #This loads a value from the section "cosmological_parameters" that we read above.
    omega_m = block[cosmo, "omega_m"]

    # Do the main calculation that is the purpose of this module.
    # It is good to make this execute function as simple as possible
    cluster_mass = my_calculation.compute_something(omega_m, loaded_data)

    # Now we have got a result we save it back to the block like this.
    block[cosmo, "cluster_mass"] = cluster_mass

    #We tell CosmoSIS that everything went fine by returning zero
    return 0




def cleanup(config):
    # Usually python modules do not need to do anything here.
    # We just leave it in out of pedantic completeness.
    pass
