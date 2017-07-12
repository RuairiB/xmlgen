import xml.etree.cElementTree as ET
import os
import sys
import itertools
from heapq import nsmallest

sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/"))
from utils import *
from init import *
from tasks import *

sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/logscraper/"))
from logutils import *
from bestfits import *
from fitparams import *

def gen_aspect_fit(flav):
    corr_paths = []
    for p in range(0, 5):
        corr_paths.append("/latticeQCD/raid6/ruairi/freeparticle_energies/SH_fits/32^3/" + flav + "/energies/" + flav + "_32_860_PSQ" + str(p) + "_jack")

    proj_name = "anisotropy32_" + str(flav) + "_jack"
    inputdir = "/latticeQCD/raid6/ruairi/freeparticle_energies/aspect_ratio/"
    logfile = inputdir + "log_anisotropy32_" + str(flav) + "_jack.log"

    root = ET.Element("SigMonD")
    tree = ET.ElementTree(root)

    init = ET.SubElement(root, "Initialize")
    tasks = ET.SubElement(root, "TaskSequence")

    # Usage:
    # initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type)

    initialize(init, corr_paths, proj_name, logfile, "Jackknife", "32_860", "samplings")

    results = []
    # Tasks
    mucho_fits = allfits("/latticeQCD/raid6/ruairi/freeparticle_energies/SH_fits")

    # for flav in ["pion", "kaon", "eta", "nucleon"]:
    plenty_fits = []
    for x in mucho_fits:
        if "32" in x.ensemble and x.sampling == "Jackknife" and x.flav == flav: # and float(x.chisq_full) < 2.0:
            plenty_fits.append(x)
    print(len(plenty_fits))
    plenty_fits.sort(key=lambda k: (k.psq))

    fitcombos = [nsmallest(7, list(group), key=lambda x: abs(float(x.chisq_full) - 1)) for k, group in itertools.groupby(sorted(plenty_fits, key=lambda x: x.psq), lambda x: x.psq)]
    
    # # Results in too many combinations for more than ~50 fits, kills the RAM. Pity, the cartesian product function is nice...
    fitcombos = itertools.product(*fitcombos)
    print("here")
    for i,fits in enumerate(fitcombos):
        if len(fits) > 5:
            print("too many energies for " + flav)
            sys.exit()

        energies = []
        for x in fits:
            # print(x.psq)
            energies.append(x.fitname)

        aspect_ratio(tasks, 32, energies, flav + "32_" + str(i) + "_jack", inputdir + "fits/" + flav + "/" + flav + "32_dispersion_" + str(flav) + "_" + str(i) + "_jack.agr", "LMDer", "Jackknife")

    indent(root)
    filename = str(inputdir + "input_anisotropy32_" + str(flav) + "_jack.xml")
    tree.write(filename)

if __name__ == "__main__":
    for flav in ["pion", "kaon", "eta", "nucleon"]:
        gen_aspect_fit(flav)
