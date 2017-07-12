import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/latticeQCD/raid8/laph/clover_s32_t256_ud860_s743/special/uu_mesons/"]
proj_name = "fit_32_860_eta_uu_meson_PSQ0"
inputdir = "/latticeQCD/raid6/ruairi/freeparticle_energies/SH_fits/32^3/eta/"
logfile = inputdir + "log_fit_32_860_eta_uu_meson_PSQ0_boot.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "32_860", "BLCorr")

energies = []

# Fitting
tsse = "TimeSymSingleExponential"
tsseC = "TimeSymSingleExponentialPlusConstant"
tste = "TimeSymTwoExponential"
tsteC = "TimeSymTwoExponentialPlusConstant"
tsgs = "TimeSymGeomSeriesExponential"

# Tasks
# dofit(tasks, optype, operator, tmin, tmax, fitfn, plotfile, psq, energies, "E1_kaon_4_35P0tsgs", sampling="Bootstrap")
# writesamplings(tasks, energies, energyfile, sampling="Bootstrap")

readsamplings(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/refenergies/kaon32_PSQ0_reference_bins_boot", "Bootstrap", ["E1_kaon_4_35P0tsgs"])
#Time symmetric single exponential
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 3):
        dofit(tasks, "eta P=(0,0,0) A1up_1 SS_0", "eta", str(tmin), str(tmax), tsse, "LMDer", inputdir + "fits/PSQ0/eta_32_860_PSQ0_tsse_tmin" + str(tmin) + "tmax" + str(tmax) + "_boot.agr", "0", energies, "E1_kaon_4_35P0tsgs", "Bootstrap", "16")
        tmin+=1
    tmax-=1
    tmin=3

#Time symmetric single exponential + C
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 3):
        dofit(tasks, "eta P=(0,0,0) A1up_1 SS_0", "eta", str(tmin), str(tmax), tsseC, "LMDer", inputdir + "fits/PSQ0/eta_32_860_PSQ0_tsseC_tmin" + str(tmin) + "tmax" + str(tmax) + "_boot.agr", "0", energies, "E1_kaon_4_35P0tsgs", "Bootstrap", "16")
        tmin+=1
    tmax-=1
    tmin=3

#Time symmetric single exponential
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 3):
        dofit(tasks, "eta P=(0,0,0) A1up_1 SS_0", "eta", str(tmin), str(tmax), tsgs, "LMDer", inputdir + "fits/PSQ0/eta_32_860_PSQ0_tsgs_tmin" + str(tmin) + "tmax" + str(tmax) + "_boot.agr", "0", energies, "E1_kaon_4_35P0tsgs", "Bootstrap", "16")
        tmin+=1
    tmax-=1
    tmin=3

    
writesamplings(tasks, energies, inputdir + "energies/eta_32_860_PSQ0_boot", sampling="Bootstrap")
    
indent(root)
filename = str(inputdir + "input_fit_32_860_eta_uu_meson_PSQ0_boot.xml")
tree.write(filename)
