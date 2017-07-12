import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/latticeQCD/raid7/laph/clover_s24_t128_ud840_s743/special/uu_mesons/"]
proj_name = "momavg_eta24"
inputdir = "/latticeQCD/raid6/ruairi/freeparticle_energies/mom_averaging/"
logfile = inputdir + "log_momavg_eta24.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "24_840", "BLCorr")

# momaverage(tasks, oplist, psq, binfile, tmin, tmax, hermitian)
momaverage(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/run_scripts/opdefs_24_840_uu.rb", 1, inputdir + "avgbins/avgcorr_24_840_uu_mesons_PSQ1", 3, 40, True)
momaverage(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/run_scripts/opdefs_24_840_uu.rb", 2, inputdir + "avgbins/avgcorr_24_840_uu_mesons_PSQ2", 3, 40, True)
momaverage(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/run_scripts/opdefs_24_840_uu.rb", 3, inputdir + "avgbins/avgcorr_24_840_uu_mesons_PSQ3", 3, 40, True)
momaverage(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/run_scripts/opdefs_24_840_uu.rb", 4, inputdir + "avgbins/avgcorr_24_840_uu_mesons_PSQ4", 3, 40, True)
# momaverage(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/run_scripts/opdefs_24_840_uu.rb", 5, inputdir + "avgbins/avgcorr_24_840_uu_mesons_PSQ5", 3, 40, True)
# momaverage(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/run_scripts/opdefs_24_840_uu.rb", 6, inputdir + "avgbins/avgcorr_24_840_uu_mesons_PSQ6", 3, 40, True)

    
indent(root)
tree.write(inputdir + "input_momavg_eta24.xml")
