import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/home/ruairi/research/freeparticle_energies/mom_averaging/avgbins/avgcorr_32_860_uud_baryons_PSQ1", "/home/ruairi/research/freeparticle_energies/mom_averaging/avgbins/avgcorr_32_860_uud_baryons_PSQ2", "/home/ruairi/research/freeparticle_energies/mom_averaging/avgbins/avgcorr_32_860_uud_baryons_PSQ3", "/home/ruairi/research/freeparticle_energies/mom_averaging/avgbins/avgcorr_32_860_uud_baryons_PSQ4"]
proj_name = "irrepavg_nucleon32"
inputdir = "/home/ruairi/research/freeparticle_energies/irrep_averaging/"
logfile = inputdir + "log_irrepavg_nucleon32_moving.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "32_860", "bins")

# operatoraverage(tasks, ops, opresult, binfile, tmin, tmax, hermitian)
oplist = ["isodoublet P=(0,0,1) G1_1 SS_0", "isodoublet P=(0,0,1) G1_2 SS_0"]
operatoraverage(tasks, oplist, "isodoublet P=(0,0,1) G1_1 SS_0", inputdir + "avgbins/irrepavg_32_860_uud_baryons_PSQ1", 3, 40, True)

oplist = ["isodoublet P=(0,1,1) G_1 SS_0", "isodoublet P=(0,1,1) G_2 SS_0"]
operatoraverage(tasks, oplist, "isodoublet P=(0,1,1) G_1 SS_0", inputdir + "avgbins/irrepavg_32_860_uud_baryons_PSQ2", 3, 40, True)

oplist = ["isodoublet P=(1,1,1) G_1 SS_0", "isodoublet P=(1,1,1) G_2 SS_0"]
operatoraverage(tasks, oplist, "isodoublet P=(1,1,1) G_1 SS_0", inputdir + "avgbins/irrepavg_32_860_uud_baryons_PSQ3", 3, 40, True)

oplist = ["isodoublet P=(0,0,2) G1_1 SS_0", "isodoublet P=(0,0,2) G1_2 SS_0"]
operatoraverage(tasks, oplist, "isodoublet P=(0,0,2) G1_1 SS_0", inputdir + "avgbins/irrepavg_32_860_uud_baryons_PSQ4", 3, 40, True)

indent(root)
tree.write(inputdir + "input_irrepavg_nucleon32_moving.xml")
