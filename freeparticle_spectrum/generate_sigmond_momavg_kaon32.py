import xml.etree.cElementTree as ET
import os
from utils import *
from init import *
from tasks import *

corr_paths = ["/home/ruairi/research/correlator_data/clover_s32_t256_ud860_s743/special/su_mesons/"]
proj_name = "momavg_kaon32"
inputdir = "/home/ruairi/research/freeparticle_energies/mom_averaging/"
logfile = inputdir + "log_momavg_kaon32.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "32_860", "BLCorr")

momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_32_860_su.rb", 1, inputdir + "avgbins/avgcorr_32_860_su_mesons_PSQ1", 3, 40, True)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_32_860_su.rb", 2, inputdir + "avgbins/avgcorr_32_860_su_mesons_PSQ2", 3, 40, True)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_32_860_su.rb", 3, inputdir + "avgbins/avgcorr_32_860_su_mesons_PSQ3", 3, 40, True)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_32_860_su.rb", 4, inputdir + "avgbins/avgcorr_32_860_su_mesons_PSQ4", 3, 40, True)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_32_860_su.rb", 5, inputdir + "avgbins/avgcorr_32_860_su_mesons_PSQ5", 3, 40, True)
momaverage(tasks, "/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_32_860_su.rb", 6, inputdir + "avgbins/avgcorr_32_860_su_mesons_PSQ6", 3, 40, True)

    
indent(root)
tree.write(inputdir + "input_momavg_kaon32.xml")
