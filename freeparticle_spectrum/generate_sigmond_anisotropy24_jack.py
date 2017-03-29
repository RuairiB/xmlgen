import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/"))
from utils import *
from init import *
from tasks import *

sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/logscraper/"))
from logutils import *
from bestfits import *

corr_paths = []
for flav in "pion", "kaon", "eta", "nucleon":
    for p in range(0, 5):
        corr_paths.append("/latticeQCD/raid6/ruairi/freeparticle_energies/SH_fits/24^3/" + flav + "/energies/" + flav + "_24_840_PSQ" + str(p) + "_jack")

proj_name = "anisotropy24_jack"
inputdir = "/latticeQCD/raid6/ruairi/freeparticle_energies/aspect_ratio/"
logfile = inputdir + "log_anisotropy24_jack.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_paths, proj_name, logfile, "Jackknife", "24_840", "samplings")

results = []
# Tasks
best = bestfits("/latticeQCD/raid6/ruairi/freeparticle_energies/SH_fits")

for flav in ["pion", "kaon", "eta", "nucleon"]:
    fits = []
    for x in best:
        if "24" in x.ensemble and x.sampling == "Jackknife" and x.flav == flav:
            fits.append(x)

    fits.sort(key=lambda k: (k.psq))

    if len(fits) > 5:
        print("too many energies for " + flav)
        sys.exit()

    energies = []
    for x in fits:
        energies.append(x.fitname)
    
    aspect_ratio(tasks, 24, energies, flav + "24_jack", "fits/" + flav + "24_dispersion_jack.agr", "Jackknife")

#writesamplings(tasks, energies, inputdir + "samplings/24_840_PSQ0_jack", sampling="Jackknife")
    
indent(root)
filename = str(inputdir + "input_anisotropy24_jack.xml")
tree.write(filename)
