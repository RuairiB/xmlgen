import xml.etree.cElementTree as ET
import os
import sys
from utils import *
from init import *
from tasks import *

sys.path.append(os.path.abspath("/home/ruairi/research/freeparticle_energies/logscraper/"))
from logutils import *
from bestfits import *

corr_paths = []
for flav in "pion", "kaon", "eta", "nucleon":
    for p in range(0, 5):
        corr_paths.append("/home/ruairi/research/freeparticle_energies/SH_fits/24^3/" + flav + "/energies/" + flav + "_24_840_PSQ" + str(p) + "_boot")

proj_name = "anisotropy24_boot"
inputdir = "/home/ruairi/research/freeparticle_energies/aspect_ratio/"
logfile = inputdir + "log_anisotropy24_boot.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "24_840", "samplings")

results = []
# Tasks
best = bestfits("/home/ruairi/research/freeparticle_energies/SH_fits")

for flav in ["pion", "kaon", "eta", "nucleon"]:
    fits = []
    for x in best:
        if "24" in x.ensemble and x.sampling == "Bootstrap" and x.flav == flav:
            fits.append(x)

    fits.sort(key=lambda k: (k.psq))

    if len(fits) > 5:
        print("too many energies for " + flav)
        sys.exit()

    energies = []
    for x in fits:
        energies.append(x.fitname)
    
    aspect_ratio(tasks, 24, energies, flav + "24_boot", "fits/" + flav + "24_dispersion_boot.agr", "Bootstrap")


#writesamplings(tasks, energies, inputdir + "samplings/24_840_PSQ0_boot", sampling="Bootstrap")
    
indent(root)
filename = str(inputdir + "input_anisotropy24_boot.xml")
tree.write(filename)
