import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/latticeQCD/raid8/laph/clover_s32_t256_ud860_s743/special/uud_baryons/"]
proj_name = "momavg_nucleon32"
inputdir = "/latticeQCD/raid6/ruairi/freeparticle_energies/mom_averaging/"
logfile = inputdir + "log_momavg_nucleon32.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "32_860", "BLCorr")

# momaverage(tasks, oplist, psq, binfile, tmin, tmax, hermitian)
momaverage(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/run_scripts/opdefs_32_860_uud.rb", 1, inputdir + "avgbins/avgcorr_32_860_uud_baryons_PSQ1", 3, 40, True)
momaverage(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/run_scripts/opdefs_32_860_uud.rb", 2, inputdir + "avgbins/avgcorr_32_860_uud_baryons_PSQ2", 3, 40, True)
momaverage(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/run_scripts/opdefs_32_860_uud.rb", 3, inputdir + "avgbins/avgcorr_32_860_uud_baryons_PSQ3", 3, 40, True)
momaverage(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/run_scripts/opdefs_32_860_uud.rb", 4, inputdir + "avgbins/avgcorr_32_860_uud_baryons_PSQ4", 3, 40, True)
# momaverage(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/run_scripts/opdefs_32_860_uud.rb", 5, inputdir + "avgbins/avgcorr_32_860_uud_baryons_PSQ5", 3, 40, True)
# momaverage(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/run_scripts/opdefs_32_860_uud.rb", 6, inputdir + "avgbins/avgcorr_32_860_uud_baryons_PSQ6", 3, 40, True)

    
indent(root)
tree.write(inputdir + "input_momavg_nucleon32.xml")
