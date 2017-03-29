import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/latticeQCD/raid6/ruairi/freeparticle_energies/SH_fits/32^3/kaon/energies/kaon_32_860_PSQ0_boot"]
proj_name = "refenergy_kaon32"
inputdir = "/latticeQCD/raid6/ruairi/freeparticle_energies/refenergies/"
logfile = inputdir + "log_refenergy_kaon32.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "32_860", "samplings")

writesamplings(tasks, ["E1_tmin8tmax34P0tsgs"], inputdir + "kaon32_PSQ0_reference_bins", "Bootstrap")

    
indent(root)
tree.write(inputdir + "input_ref_kaon32.xml")
