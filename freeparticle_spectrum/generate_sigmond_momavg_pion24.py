import xml.etree.cElementTree as ET
import os
sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/home/ruairi/research/correlator_data/clover_s24_t128_ud840_s743/special/du_mesons/"]
proj_name = "momavg_pion24"
inputdir = "/home/ruairi/research/freeparticle_energies/mom_averaging/"
logfile = inputdir + "log_momavg_pion24.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "24_840", "BLCorr")

# momaverage(tasks, oplist, psq, binfile, tmin, tmax, hermitian)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_24_840_du.rb", 1, inputdir + "avgbins/avgcorr_24_840_du_mesons_PSQ1", 3, 40, True)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_24_840_du.rb", 2, inputdir + "avgbins/avgcorr_24_840_du_mesons_PSQ2", 3, 40, True)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_24_840_du.rb", 3, inputdir + "avgbins/avgcorr_24_840_du_mesons_PSQ3", 3, 40, True)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_24_840_du.rb", 4, inputdir + "avgbins/avgcorr_24_840_du_mesons_PSQ4", 3, 40, True)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_24_840_du.rb", 5, inputdir + "avgbins/avgcorr_24_840_du_mesons_PSQ5", 3, 40, True)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_24_840_du.rb", 6, inputdir + "avgbins/avgcorr_24_840_du_mesons_PSQ6", 3, 40, True)

    
indent(root)
tree.write(inputdir + "input_momavg_pion24.xml")
