import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/latticeQCD/raid8/laph/clover_s32_t256_ud860_s743/special/du_mesons/", "/latticeQCD/raid8/laph/clover_s32_t256_ud860_s743/special/su_mesons/", "/latticeQCD/raid8/laph/clover_s32_t256_ud860_s743/special/uu_mesons/"]
proj_name = "momavg_test"
# inputdir = "/latticeQCD/raid6/ruairi/freeparticle_energies/SH_fits/32^3/pion/"
logfile = "log_momavg_test.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "32_860", "BLCorr")

# momaverage(tasks, oplist, psq, binfile, tmin, tmax, hermitian)
momaverage(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/run_scripts/opdefs_32_860_du.rb", 1, "averagedbins_test", 3, 40, True) 

    
indent(root)
filename = str("input_momavg_test.xml")
tree.write(filename)
