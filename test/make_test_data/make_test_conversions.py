import numpy as np
import sys, os
import matplotlib.pyplot as plt
import itertools
from colossus.cosmology import cosmology
from colossus.halo.mass_defs import changeMassDefinition


def save_test_data(data, fname, header_line2, done=False):
    header = "Computed using python\n" + header_line2
    if done:
        testfilepath1 = '../data'
        np.savetxt(os.path.join(testfilepath1, fname), data, header=header)
    print(header)
    print(data)


def make_grid(all_lists, ntruth):
    ncols = len(all_lists)+ntruth
    nrows = np.prod([len(x) for x in all_lists])

    combos = -1.0*np.ones(shape=(nrows, ncols))
    combogenerator = itertools.product(*all_lists)
    for i, row in zip(range(nrows), combogenerator):
        combos[i,:-ntruth] = row
    return combos


def test_convert_c(targs):
    cosmology.setCosmology('myCosmo', {'flat': False, 'H0': 70., 'Om0': targs['omm'],
                                       'Ode0': targs['oml'], 'Ob0': 0.05, 'sigma8': 0.8,
                                       'ns': 0.96, 'relspecies':False})

    cosmo = {'omega_m': targs['omm'], 'omega_k': 1.0 - targs['omm'] - targs['oml'],
             'omega_l': targs['oml']}
    out = changeMassDefinition(targs['m1'], targs['c1'], targs['z'], targs['m1def'], targs['m2def'])
    m2, r2, c2 = out
    return c2
    

def test_convert_m(targs):
    cosmology.setCosmology('myCosmo', {'flat': False, 'H0': 70., 'Om0': targs['omm'],
                                       'Ode0': targs['oml'], 'Ob0': 0.05, 'sigma8': 0.8,
                                       'ns': 0.96, 'relspecies':False})
    colcosmo = cosmology.getCurrent()

    cosmo = {'omega_m': targs['omm'], 'omega_k': 1.0 - targs['omm'] - targs['oml'],
             'omega_l': targs['oml']}
    out = changeMassDefinition(targs['m1'], targs['c1'], targs['z'], targs['m1def'], targs['m2def'])
    m2, r2, c2 = out

    if targs['m1def'][-1] == targs['m2def'][-1]:
        densityratio = 1.0
    elif targs['m1def'][-1] == 'c':
        densityratio = targs['omm'] * (1. + targs['z'])**3 / colcosmo.Ez(targs['z'])**2
    elif targs['m1def'][-1] == 'm':
        densityratio = colcosmo.Ez(targs['z'])**2 / (targs['omm'] * (1. + targs['z'])**3)
    return targs['m1'] * densityratio \
           * float(targs['m2def'][:-1])/float(targs['m1def'][:-1]) * (c2/targs['c1'])**3


def main():
    # =============================================
    # Module settings
    truthfuncs = [test_convert_c, test_convert_m]
    modulename = 'conversions'
    header2 = "M1\tc1\tz\tOmM\tOmL\tc2truth\tm2truth"
    done = True

    # =============================================
    # Set ranges
    m1list = np.logspace(14, 15, 10)
    c1list = np.linspace(2, 7, 5)
    zlist = np.linspace(0.2, 0.7, 6)
    ommlist = np.linspace(0.15, 0.45, 5)
    omllist = 1.0 - ommlist
    all_lists = [m1list, c1list, zlist, ommlist, omllist]

    m1deflist = ['200m', '200c']
    m2deflist = ['200m', '500c']


    # =============================================
    # Make truth files
    mdefcombos = itertools.product(m1deflist, m2deflist)
    for m1def, m2def in mdefcombos:
        # =============================================
        # Make the grid of truth values
        ntruth = len(truthfuncs)
        combos = make_grid(all_lists, ntruth)
        for i in range(ntruth):
            for row in combos:
                truthargs = {'m1':row[0], 'c1':row[1], 'z':row[2], 'omm':row[3], 'oml':row[4],
                             'm1def':m1def, 'm2def':m2def}
                row[-(ntruth-i)] = truthfuncs[i](truthargs)

        # =============================================
        # Drop the lines with prob < 1e-20
        # for i in range(ntruth):
        #     combos = combos[np.where(combos[:,-(i+1)] > 1.e-20)]

        # =============================================
        # Make sure that we have the same columns as colnames
        headergood = len(header2.split('\t')) == len(all_lists)+len(truthfuncs)
        if not headergood and done:
            raise ValueError("Column labels do not match combo table")
        if not headergood:
            print("=============================")
            print("Be sure to update the header!")
            print("=============================")
        else:
            print("Header looks good")


        # =============================================
        # Save to a file
        fname = 'test_' + modulename + '_' + m1def + '_to_' + m2def + '.txt'
        print(fname)
        save_test_data(combos, fname, header2, done=done)




if __name__ == "__main__":
    main()
