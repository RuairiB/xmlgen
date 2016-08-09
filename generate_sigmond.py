import xml.etree.cElementTree as ET
import os
from init import *
from tasks import *

# corr_path = "/latticeQCD/raid8/laph/clover_s32_t256_ud860_s743/bosonic_correlators/isodoublet_strange/mom_0_0_0/T1u_1/"
corr_path = "test_data/"
oplist_file = "oplist.txt"
proj_name = "pro-jekt"
logfile = "good-filename.log"
file_tail = "isospin_etc"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

initialize(corr_path, oplist_file, proj_name, logfile, init)

# Task variables
mintime = 3
maxtime = 26
norm_time = 3
metric_time = 4
diag_time = 6
cond_num = "1e-3"

# Tasks
oldrotateA(mintime, maxtime, proj_name, file_tail, norm_time, metric_time, diag_time, cond_num, tasks)
oldrotateB(mintime, maxtime, proj_name, file_tail, tasks)

indent(root)
tree.write("filename.xml")
