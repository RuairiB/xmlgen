import os
import sys
from parse_explevels import *
from levelutils import *

sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/"))
from utils import *
from init import *
from tasks import *

sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/logscraper/"))
from logutils import *
from bestfits import *
from thresholds import supers

ISO_MAP = {
    'I=0': 'singlet',
    '2I=1': 'doublet',
    'I=1': 'triplet',
    '2I=3': 'quartet',
    'I=2': 'quintet',
    '2I=5': 'sextet'
}

crap = supers("/home/ruairi/research/freeparticle_energies/spectra/")
ones = []
twos = []
threes = []
fours = []
for x in crap:
    if x.numpart == 1:
        ones.append(x)
    elif x.numpart == 2:
        twos.append(x)
    elif x.numpart == 3:
        threes.append(x)
    elif x.numpart == 4:
        fours.append(x)
    else:
        print("have " + str(x.numpart) + " particles in one/some of the logs")
        sys.exit()

basedir = "/home/ruairi/research/expectedlevels/" # eg: + "24^3_390/mom_000/bosonic_I=1_S=0_levels.txt"

sampling = "Bootstrap"
samp = "boot"

f3 = open("/home/ruairi/research/thresholds3.py", 'w')
f4 = open("/home/ruairi/research/thresholds4.py", 'w')

f3.write(r'# Ensemble, PSQ, type, I, S, Irrep')
f4.write(r'# Ensemble, PSQ, type, I, S, Irrep')

f3.write("\nTHREE_PARTICLE_ENERGIES = {\n")
f4.write("\nFOUR_PARTICLE_ENERGIES = {\n")

countE = 0
for ensem,ensemble in [("32^3_240/", "32_860"), ("24^3_390/", "24_840")]:
    if countE != 0:
        f3.write(",\n")
        f4.write(",\n")
    countE += 1

    # PRINT_ENSEMBLE:
    if ensemble == "32_860":
        f3.write("    \'clover_s32_t256_ud860_s743\': {\n")
        f4.write("    \'clover_s32_t256_ud860_s743\': {\n")
    elif ensemble == "24_840":
        f3.write("    \'clover_s24_t128_ud840_s743\': {\n")
        f4.write("    \'clover_s24_t128_ud840_s743\': {\n")
    else:
        print("What ensemble are you " + ensemble + "?")

    countP = 0
    for mom,psq in [("mom_000/", 0), ("mom_001/", 1), ("mom_011/", 2), ("mom_111/", 3), ("mom_002/", 4)]:
        if countP != 0:
            f3.write(",\n")
            f4.write(",\n")
        countP += 1

        # PRINT_PSQ:
        f3.write("        " + str(psq) + ": {\n")
        f4.write("        " + str(psq) + ": {\n")

        files = [y for x in os.walk(basedir + ensem + mom) for y in glob(os.path.join(x[0], '*.txt'))]

        bosonic = []
        fermionic = []
        for f in files:
            if 'bosonic' in f:
                bosonic.append(f)
            elif 'fermionic' in f:
                fermionic.append(f)
            else:
                print("what spin type are you " + f + "?")
        # loop over spins/type
        countT = 0
        for spin,spun in [(bosonic, 'boson'), (fermionic, 'fermion')]:
            if countT != 0:
                f3.write(",\n")
                f4.write(",\n")
            countT += 1


            f3.write("            \'" + spun + "\': {\n")
            f4.write("            \'" + spun + "\': {\n")
            isolist = [('singlet', []),
                       ('doublet', []),
                       ('triplet', []),
                       ('quartet', []),
                       ('quintet', []),
                       ('sextet', [])]

            # split spin by isospin
            for x in spin:
                iso = ISO_MAP[x.split("/")[-1].split("_")[1]]
                if iso == 'singlet':
                    isolist[0][1].append(x)
                elif iso == 'doublet':
                    isolist[1][1].append(x)
                elif iso == 'triplet':
                    isolist[2][1].append(x)
                elif iso == 'quartet':
                    isolist[3][1].append(x)
                elif iso == 'quintet':
                    isolist[4][1].append(x)
                elif iso == 'sextet':
                    isolist[5][1].append(x)

            # loop over isospin
            countI = 0
            for I in isolist:
                if countI != 0:
                    f3.write(",\n")
                    f4.write(",\n")
                countI += 1


                f3.write("                \'" + I[0] + "\': {\n")
                f4.write("                \'" + I[0] + "\': {\n")
                # loop over strangeness
                countS = 0
                for f in I[1]:
                    if countS != 0:
                        f3.write(",\n")
                        f4.write(",\n")
                    countS += 1

                    f3.write("                    " + f.split("/")[-1].split("_")[2][-1] + ": {\n")
                    f4.write("                    " + f.split("/")[-1].split("_")[2][-1] + ": {\n")

                    # loop over irreps:
                    irreps = readlevels(f, ensemble, psq, empties=True) # list of irreps

                    pullenergies(irreps, ones, twos, threes, fours, ensemble, sampling, ignore_empties=True)
                    count = 0
                    for irrep in irreps:
                        if count != 0:
                            f3.write(",\n")
                            f4.write(",\n")
                        count += 1

                        if len(irrep) == 1 and irrep[0].Npart == 0:
                            f3.write("                        \'" + irrep[0].irrep + "\': []")
                            f4.write("                        \'" + irrep[0].irrep + "\': []")
                        else:
                        # if True:
                            threshold3 = irrep_threshold(irrep, 3)
                            threshold4 = irrep_threshold(irrep, 4)
                            if threshold3:
                                f3.write("                        \'" + threshold3.irrep + "\': (r\"$" + threshold3.resultstr_tex + "$\", " + threshold3.energy + ", " + threshold3.energyerr + ")")
                            else:
                                f3.write("                        \'" + irrep[0].irrep + "\': []")
                            if threshold4:
                                f4.write("                        \'" + threshold4.irrep + "\': (r\"$" + threshold4.resultstr_tex + "$\", " + threshold4.energy + ", " + threshold4.energyerr + ")")
                            else:
                                f4.write("                        \'" + irrep[0].irrep + "\': []")

                    # close strangeness
                    f3.write("\n                    }")
                    f4.write("\n                    }")
                # close isospin
                f3.write("\n                }")
                f4.write("\n                }")
            # close spin
            f3.write("\n            }")
            f4.write("\n            }")
        # close PSQ
        f3.write("\n        }")
        f4.write("\n        }")
    # close ensemble
    f3.write("\n    }")
    f4.write("\n    }")
# close it all
f3.write("\n}\n")
f4.write("\n}\n")
