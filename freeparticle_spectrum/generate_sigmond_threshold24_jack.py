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
        corr_paths.append("/home/ruairi/research/freeparticle_energies/SH_fits/24^3/" + flav + "/energies/" + flav + "_24_840_PSQ" + str(p) + "_jack")
        proj_name = "twoparticles24_jack"
        inputdir = "/home/ruairi/research/freeparticle_energies/thresholds/"
        logfile = inputdir + "log_thresholds24_jack.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

initialize(init, corr_paths, proj_name, logfile, "Jackknife", "24_840", "samplings", "True")

# Tasks
refmass_name = "E1_ref_5_35P0tsgs"

fudge = ["E1_kaon_4_35P0tsgs",
         "E1_kaon_4_35P1tsgs",
         "E1_kaon_4_35P2tsgs",
         "E1_kaon_4_35P3tsgs",
         "E1_kaon_3_35P4tsgs",
         "E1_pion_4_35P0tsgs",
         "E1_pion_4_35P1tsgs",
         "E1_pion_4_35P2tsgs",
         "E1_pion_3_35P3tsgs",
         "E1_pion_4_35P4tsgs",
         "E1_nucleon_3_25P0tsgs",
         "E1_nucleon_3_25P1tsgs",
         "E1_nucleon_3_25P2tsgs",
         "E1_nucleon_3_25P3tsgs",
         "E1_nucleon_3_25P4tsgs",
         "E1_eta_17_25P0tsseC",
         "E1_eta_17_25P1tsseC",
         "E1_eta_17_25P2tsseC",
         "E1_eta_17_25P3tsseC"]

fits = []
for delight in fudge:
    temp = fitlog()
    temp.fitname = delight
    # temp.stripindex()
    temp.psqfromfitname()
    temp.findflavfitname()
    fits.append(temp)

# Two particle energy combinations:
pairs = list(itertools.combinations(fits, 3))

for c in fits:
    pairs.append(tuple((c, c, c))) # include \pi \pi, \eta \eta, etc states

energies = []
# add_obs(tasks, fits, "result_str", "Jackknife")
for x in pairs:
    temp = []
    # add_obs(tasks, pair_of_fitnames, result_str_from_pair_params, "Jackknife")
    result = threepart_fitname(x, "none")
    energies.append(result)
    energies.append(result + "_ref")

    temp.append(x[0].fitname)
    temp.append(x[1].fitname)
    add_obs(tasks, temp, result, "Jackknife")
    ref_ratio(tasks, result, refmass_name, result + "_ref", "Jackknife")

writesamplings(tasks, energies, inputdir + "energies/thresholds24_jack", sampling="Jackknife")

indent(root)
filename = str(inputdir + "input_thresholds24_jack.xml")
tree.write(filename)
