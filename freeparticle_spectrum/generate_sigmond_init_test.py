import xml.etree.cElementTree as ET
import os
from utils import *
from init import *
from tasks import *

corr_paths = ["/home/ruairi/research/correlator_data/clover_s32_t256_ud860_s743/special/du_mesons/", "/home/ruairi/research/correlator_data/clover_s32_t256_ud860_s743/special/su_mesons/", "/home/ruairi/research/correlator_data/clover_s32_t256_ud860_s743/special/uu_mesons/"]
proj_name = "init_test"
# inputdir = "/home/ruairi/research/freeparticle_energies/SH_fits/32^3/pion/"
logfile = "log_init_test.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
# tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "32_860", "BLCorr")

    
indent(root)
filename = str("input_init_test.xml")
tree.write(filename)
