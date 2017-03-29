import xml.etree.cElementTree as ET
import os
sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/home/ruairi/research/correlator_data/clover_s24_t128_ud840_s743/special/uud_baryons/"]
proj_name = "momavg_nucleon24"
inputdir = "/home/ruairi/research/freeparticle_energies/mom_averaging/"
logfile = inputdir + "log_momavg_nucleon24.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "24_840", "BLCorr")

# momaverage(tasks, oplist, psq, binfile, tmin, tmax, hermitian)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_24_840_uud.rb", 1, inputdir + "avgbins/avgcorr_24_840_uud_baryons_PSQ1", 3, 40, True)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_24_840_uud.rb", 2, inputdir + "avgbins/avgcorr_24_840_uud_baryons_PSQ2", 3, 40, True)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_24_840_uud.rb", 3, inputdir + "avgbins/avgcorr_24_840_uud_baryons_PSQ3", 3, 40, True)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_24_840_uud.rb", 4, inputdir + "avgbins/avgcorr_24_840_uud_baryons_PSQ4", 3, 40, True)
# momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_24_840_uud.rb", 5, inputdir + "avgbins/avgcorr_24_840_uud_baryons_PSQ5", 3, 40, True)
# momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_24_840_uud.rb", 6, inputdir + "avgbins/avgcorr_24_840_uud_baryons_PSQ6", 3, 40, True)

    
indent(root)
tree.write(inputdir + "input_momavg_nucleon24.xml")
