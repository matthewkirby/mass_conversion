"""Classes to define different concentration-mass relations"""
import mass_conversion.utils as utils
import mass_conversion.conversions as conv


class ConcentrationModel(object):
    """This is the base class for each cM model"""
    def __init__(self, name, model_mdef, mask, cosmology, note):
        self.name = name
        self.model_mdef = model_mdef # Mass definition that the model is defined in
        self.mask = mask # Dict mmin/mmax zmin/zmax can be None
        self.cosmology = cosmology # Defined in a specific cosmology
        self.note = note

    def __call__(self, m1list, m1def):
        """Given m1 in m1def, compute concentration in m1def"""
        raise NotImplementedError("c-M relation for {} is not yet implemented".format(self.name))

    def __repr__(self):
        line1 = 'Concentration-Mass relation from {}\n'.format(self.name)
        line2 = 'Defined for mass definition(s): {}\n'.format(self.model_mdef)
        line3 = 'With masses and redshifts in {}\n'.format(str(self.mask))
        line4 = self.note
        return line1+line2+line3+line4


class FixedC200c(ConcentrationModel):
    """For high mass clusters, concentration plateaus at c200c ~ 4.0"""
    def __init__(self, c200c):
        self.c200c = float(c200c)
        note = "Approximation for high mass clusters"
        super().__init__(name='fixedc', model_mdef='200c', mask=None,
                         cosmology=None, note=note)

    def __repr__(self):
        parent = super().__repr__()
        line1 = '\nc200c = {}\n'.format(self.c200c)
        return parent+line1

    def __call__(self, m2, z, m2def, cosmo=None):
        """Given m2 in m2def, compute concentration in m2def"""
        delta1, density1, c1 = 200., 'crit', self.c200c
        delta2, density2 = utils.parse_mdef_string(m2def)
        c2 = conv.convert_concentration(c1, z, '200c', m2def, cosmo)
        return c2

        



def main():
    cmrel = FixedC200c(4.0)
    m1 = 1e15
    z = 0.5
    m1def = '200m'
    cosmo = {'omega_m': 0.3, 'omega_k': 0.0, 'omega_l': 0.7}
    print(cmrel(m1, z, m1def, cosmo))





if __name__ == "__main__":
    main()
