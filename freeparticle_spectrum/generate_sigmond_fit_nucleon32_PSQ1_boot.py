import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/home/ruairi/research/freeparticle_energies/irrep_averaging/avgbins/irrepavg_32_860_uud_baryons_PSQ1"]
proj_name = "fit_32_860_nucleon_uud_baryon_PSQ1"
inputdir = "/home/ruairi/research/freeparticle_energies/SH_fits/32^3/nucleon/"
logfile = inputdir + "log_fit_32_860_nucleon_uud_baryon_PSQ1_boot.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "32_860", "bins")

energies = []

# Fitting
tsse = "TimeSymSingleExponential"
tsseC = "TimeSymSingleExponentialPlusConstant"
tste = "TimeSymTwoExponential"
tsteC = "TimeSymTwoExponentialPlusConstant"
tsgs = "TimeSymGeomSeriesExponential"

operator = "isodoublet P=(0,0,1) G1_1 SS_0"
psq = "1"

# Tasks
# dofit(tasks, optype, operator, tmin, tmax, fitfn, plotfile, psq, energies, "E1_kaon_4_35P0tsgs", sampling="Bootstrap")
# writesamplings(tasks, energies, energyfile, sampling="Bootstrap")

readsamplings(tasks, "/home/ruairi/research/freeparticle_energies/refenergies/kaon32_PSQ0_reference_bins_boot", "Bootstrap", ["E1_kaon_4_35P0tsgs"])
#Time symmetric single exponential
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 6):
        dofit(tasks, operator, "nucleon", str(tmin), str(tmax), tsse, "LMDer", inputdir + "fits/PSQ1/nucleon_32_860_PSQ1_tsse_tmin" + str(tmin) + "tmax" + str(tmax) + "_boot.agr", psq, energies, "E1_kaon_4_35P0tsgs", "Bootstrap")
        tmin+=1
    tmax-=1
    tmin=3

#Time symmetric two exponential    
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 10):
        dofit(tasks, operator, "nucleon", str(tmin), str(tmax), tste, "LMDer", inputdir + "fits/PSQ1/nucleon_32_860_PSQ1_tste_tmin" + str(tmin) + "tmax" + str(tmax) + "_boot.agr", psq, energies, "E1_kaon_4_35P0tsgs", "Bootstrap")
        tmin+=1
    tmax-=1
    tmin=3

#Time symmetric geometric series    
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 10):
        dofit(tasks, operator, "nucleon", str(tmin), str(tmax), tsgs, "LMDer", inputdir + "fits/PSQ1/nucleon_32_860_PSQ1_tsgs_tmin" + str(tmin) + "tmax" + str(tmax) + "_boot.agr", psq, energies, "E1_kaon_4_35P0tsgs", "Bootstrap")
        tmin+=1
    tmax-=1
    tmin=3

    
writesamplings(tasks, energies, inputdir + "energies/nucleon_32_860_PSQ1_boot", sampling="Bootstrap")
    
indent(root)
filename = str(inputdir + "input_fit_32_860_nucleon_uud_baryon_PSQ1_boot.xml")
tree.write(filename)
