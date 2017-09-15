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


crap = supers("/latticeQCD/raid6/ruairi/freeparticle_energies/spectra/")
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

basedir = "/home/ruairi/research/expectedlevels/" # eg: 24^3_390/mom_000/bosonic_I=1_S=0_levels.txt"

tableroot = "/latticeQCD/raid6/ruairi/freeparticle_energies/notes/tables/spectra/"

for ensem,ensemble in [("32^3_240/", "32_860"), ("24^3_390/", "24_840")]:
    for mom,psq in [("mom_000/", 0), ("mom_001/", 1), ("mom_011/", 2), ("mom_111/", 3), ("mom_002/", 4)]:
        files = [y for x in os.walk(basedir + ensem + mom) for y in glob(os.path.join(x[0], '*.txt'))]
        for f in files:
            for sampling,samp in [("Bootstrap", "boot"), ("Jackknife", "jack")]:
                levels = readlevels(f, ensemble, psq) # list of irreps
                # print("about to pull for: " + f)
                pullenergies(levels, ones, twos, threes, fours, ensemble, sampling)
                destination = tableroot + ensem + mom + f.split("/")[-1].strip('.txt')

                for irrep in levels:
                    if len(irrep) > 0:
                        textable_irrep(destination + "_" + irrep[0].irrep + "_" + samp, irrep, ensemble, psq, sampling)
