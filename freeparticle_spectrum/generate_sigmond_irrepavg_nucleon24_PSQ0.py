import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/home/ruairi/research/correlator_data/clover_s24_t128_ud840_s743/special/uud_baryons/"]
proj_name = "irrepavg_nucleon24"
inputdir = "/home/ruairi/research/freeparticle_energies/irrep_averaging/"
logfile = inputdir + "log_irrepavg_nucleon24_PSQ0.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "24_840", "BLCorr")

# operatoraverage(tasks, ops, opresult, binfile, tmin, tmax, hermitian)
oplist = ["nucleon P=(0,0,0) G1g_1 SS_0", "nucleon P=(0,0,0) G1g_2 SS_0"]
operatoraverage(tasks, oplist, "isodoublet P=(0,0,0) G1g_1 SS_0", inputdir + "avgbins/irrepavg_24_840_uud_baryons_PSQ0", 3, 40, True)

indent(root)
tree.write(inputdir + "input_irrepavg_nucleon24_PSQ0.xml")
