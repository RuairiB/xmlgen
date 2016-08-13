import xml.etree.cElementTree as ET
import os
from init import *
from tasks import *

# Rewrite to extract corr info (isospin, irrep, etc) from filenames
# Decide on method of parameter specification, command line args?
# Move indent fn from init.py to general XML util file?
# Extract level info for fitting from old rotation tasks?

# corr_path = "/latticeQCD/raid8/laph/clover_s32_t256_ud860_s743/bosonic_correlators/isodoublet_strange/mom_0_0_0/T1u_1/"
corr_path = "test_data/"
oplist_file = "oplist.txt"
proj_name = "pro-jekt"          # Project name = matrix name
logfile = "good-filename.log"
file_tail = "isospin_etc"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

initialize(init, corr_path, oplist_file, proj_name, logfile)

# Task variables
mintime = 3
maxtime = 26
norm_time = 3
metric_time = 4
diag_time = 6
cond_num = "1e-3"

# Fitting
level = 1
tmin = 6
tmax = 25
fitfn = "TimeSymGeomSeriesExponential"
plotfile = "plot.agr"
plotname = "Particle.energy"

# Tasks
oldrotateA(tasks, mintime, maxtime, proj_name, file_tail, norm_time, metric_time, diag_time, cond_num)
oldrotateB(tasks, mintime, maxtime, proj_name, file_tail)

readbins(tasks, "RotatedCorrelators"+file_tail)
dofit(tasks, proj_name, level, tmin, tmax, fitfn, plotfile, plotname, "Bootstrap")

dochecks_outliers(tasks, mintime, maxtime, proj_name)
dochecks_hermitian(tasks, mintime, maxtime, proj_name)


indent(root)
tree.write("filename.xml")
