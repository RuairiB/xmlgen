import os
import sys
from parse_explevels import *
from levelutils import *

sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/logscraper/"))
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

tableroot = "/home/ruairi/research/freeparticle_energies/notes/tables/spectra/"

sampling = "Bootstrap"
samp = "boot"

f3 = open("/home/ruairi/research/thresholds3.txt", 'w')
f4 = open("/home/ruairi/research/thresholds4.txt", 'w')
f3.write("THREE_PARTICLE_ENERGIES = {\n")
f4.write("FOUR_PARTICLE_ENERGIES = {\n")

for ensem,ensemble in [("32^3_240/", "32_860"), ("24^3_390/", "24_840")]:
    # PRINT_ENSEMBLE:
    if ensemble == "32_860":
        f3.write("\t\'clover\\_s32\\_t256\\_ud860\\_s743\': {\n")
        f4.write("\t\'clover\\_s32\\_t256\\_ud860\\_s743\': {\n")
    elif ensemble == "24_840":
        f3.write("\t\'clover\\_s24\\_t128\\_ud840\\_s743\': {\n")
        f4.write("\t\'clover\\_s24\\_t128\\_ud840\\_s743\': {\n")
    else:
        print("What ensemble are you " + ensemble + "?")

    for mom,psq in [("mom_000/", 0), ("mom_001/", 1), ("mom_011/", 2), ("mom_111/", 3), ("mom_002/", 4)]:
        # PRINT_PSQ:
        f3.write("\t\t" + str(psq) + ": {\n")
        f4.write("\t\t" + str(psq) + ": {\n")
        
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
        # loop over spins
        for spin,spun in [(bosonic, 'boson')]: #, (fermionic, 'fermion')]:
            f3.write("\t\t\t\'" + spun + "\': {\n")
            f4.write("\t\t\t\'" + spun + "\': {\n")
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
            for I in isolist:
                f3.write("\t\t\t\t\'" + I[0] + "\': {\n")
                f4.write("\t\t\t\t\'" + I[0] + "\': {\n")
                # loop over strangeness
                for f in I[1]:
                    f3.write("\t\t\t\t\t" + f.split("/")[-1].split("_")[2][-1] + ": {\n")
                    f4.write("\t\t\t\t\t" + f.split("/")[-1].split("_")[2][-1] + ": {\n")
            
                    # loop over irreps:
                    irreps = readlevels(f, ensemble, psq, empties=True) # list of irreps
                    print(f)
                    pullenergies(irreps, ones, twos, threes, fours, ensemble, sampling, ignore_empties=True)
                    count = 0
                    for irrep in irreps:
                        if count != 0:
                            f3.write(",\n")
                            f4.write(",\n")
                        count += 1
                        print(irrep)
                        if len(irrep) == 1 and irrep[0].Npart == 0:
                            f3.write("\t\t\t\t\t\t\'" + irrep[0].irrep + "\': []")
                            f4.write("\t\t\t\t\t\t\'" + irrep[0].irrep + "\': []")
                        else:
                        # if True:
                            threshold3 = irrep_threshold(irrep, 3)
                            threshold4 = irrep_threshold(irrep, 4)
                            if threshold3:
                                f3.write("\t\t\t\t\t\t\'" + threshold3.irrep + "\': (r\"$" + threshold3.resultstr_tex + "$\", " + threshold3.energyprint + ")")
                            else:
                                f3.write("\t\t\t\t\t\t\'" + irrep[0].irrep + "\': []")
                            if threshold4:
                                f4.write("\t\t\t\t\t\t\'" + threshold4.irrep + "\': (r\"$" + threshold4.resultstr_tex + "$\", " + threshold4.energyprint + ")")
                            else: 
                                f4.write("\t\t\t\t\t\t\'" + irrep[0].irrep + "\': []")

                    # close strangeness
                    f3.write("\n}")
                    f4.write("\n}")
                # close isospin
                f3.write("\n}")
                f4.write("\n}")
            # close spin
            f3.write("\n}")
            f4.write("\n}")
        # close PSQ
        f3.write("\n}")
        f4.write("\n}")
    # close ensemble
    f3.write("\n}")
    f4.write("\n}")
# close it all
f3.write("\n}")
f4.write("\n}")
