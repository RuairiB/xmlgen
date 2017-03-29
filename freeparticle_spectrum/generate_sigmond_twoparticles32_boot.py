import xml.etree.cElementTree as ET
import os
import itertools
import sys
sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/logscraper/"))
from logutils import *
from bestfits import *

corr_paths = []
for flav in "pion", "kaon", "eta", "nucleon":
    for p in range(0, 5):
        corr_paths.append("/home/ruairi/research/freeparticle_energies/SH_fits/32^3/" + flav + "/energies/" + flav + "_32_860_PSQ" + str(p) + "_boot")
proj_name = "twoparticles32_boot"
inputdir = "/home/ruairi/research/freeparticle_energies/two_particles/"
logfile = inputdir + "log_twoparticles32_boot.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "32_860", "samplings")

# Tasks
refmass_name = "E1_tmin8tmax34P0tsgs"
readsamplings(tasks, "/home/ruairi/research/freeparticle_energies/refenergies/kaon32_PSQ0_reference_bins_boot", "Bootstrap", [refmass_name])

best = bestfits("/home/ruairi/research/freeparticle_energies/SH_fits")
fits = []
for x in best:
    if "32" in x.ensemble and x.sampling == "Bootstrap":
        fits.append(x)

# Two particle energy combinations:
pairs = list(itertools.combinations(fits, 2))

for c in fits:
    pairs.append(tuple((c, c))) # include \pi \pi, \eta \eta, etc states

energies = []
# add_obs(tasks, fits, "result_str", "Bootstrap")
for x in pairs:
    temp = []
    # add_obs(tasks, pair_of_fitnames, result_str_from_pair_params, "Bootstrap")
    result = twopart_fitname(x, "none")
    energies.append(result)
    energies.append(result + "_ref")
    
    temp.append(x[0].fitname)
    temp.append(x[1].fitname)
    add_obs(tasks, temp, result, "Bootstrap")
    ref_ratio(tasks, result, refmass_name, result + "_ref", "Bootstrap")

writesamplings(tasks, energies, inputdir + "energies/twoparticles32_boot", sampling="Bootstrap")
    
indent(root)
filename = str(inputdir + "input_twoparticles32_boot.xml")
tree.write(filename)
