import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/latticeQCD/raid8/laph/clover_s32_t256_ud860_s743/special/su_mesons/"]
proj_name = "fit_32_860_kaon_su_meson_PSQ0"
inputdir = "/latticeQCD/raid6/ruairi/freeparticle_energies/SH_fits/32^3/kaon/"
logfile = inputdir + "log_fit_32_860_kaon_su_meson_PSQ0_jack.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_paths, proj_name, logfile, "Jackknife", "32_860", "BLCorr")

energies = []

# Fitting
tsse = "TimeSymSingleExponential"
tsseC = "TimeSymSingleExponentialPlusConstant"
tste = "TimeSymTwoExponential"
tsteC = "TimeSymTwoExponentialPlusConstant"
tsgs = "TimeSymGeomSeriesExponential"

# Tasks
# dofit(tasks, optype, operator, tmin, tmax, fitfn, plotfile, psq, energies, "E1_tmin8tmax34P0tsgs", sampling="Jackknife")
# writesamplings(tasks, energies, energyfile, sampling="Jackknife")

readsamplings(tasks, "/latticeQCD/raid6/ruairi/freeparticle_energies/refenergies/kaon32_PSQ0_reference_bins_jack", "Jackknife", ["E1_tmin8tmax34P0tsgs"])
#Time symmetric single exponential
tmin = 3
tmax = 35

while tmax > 30:
    while tmin < (tmax - 6):
        dofit(tasks, "BasicLaph", "kaon P=(0,0,0) A1u_1 SS_0", "kaon", str(tmin), str(tmax), tsse, "Minuit2", inputdir + "fits/PSQ0/kaon_32_860_PSQ0_tsse_tmin" + str(tmin) + "tmax" + str(tmax) + "_jack.agr", "0", energies, "E1_tmin8tmax34P0tsgs", "Jackknife")
        tmin+=1
    tmax-=1
    tmin=3

#Time symmetric two exponential    
tmin = 3
tmax = 35

while tmax > 30:
    while tmin < (tmax - 15):
        dofit(tasks, "BasicLaph", "kaon P=(0,0,0) A1u_1 SS_0", "kaon", str(tmin), str(tmax), tste, "Minuit2", inputdir + "fits/PSQ0/kaon_32_860_PSQ0_tste_tmin" + str(tmin) + "tmax" + str(tmax) + "_jack.agr", "0", energies, "E1_tmin8tmax34P0tsgs", "Jackknife")
        tmin+=1
    tmax-=1
    tmin=3

#Time symmetric geometric series    
tmin = 3
tmax = 35

while tmax > 30:
    while tmin < (tmax - 15):
        dofit(tasks, "BasicLaph", "kaon P=(0,0,0) A1u_1 SS_0", "kaon", str(tmin), str(tmax), tsgs, "Minuit2", inputdir + "fits/PSQ0/kaon_32_860_PSQ0_tsgs_tmin" + str(tmin) + "tmax" + str(tmax) + "_jack.agr", "0", energies, "E1_tmin8tmax34P0tsgs", "Jackknife")
        tmin+=1
    tmax-=1
    tmin=3

    
writesamplings(tasks, energies, inputdir + "energies/kaon_32_860_PSQ0_jack", sampling="Jackknife")
    
indent(root)
filename = str(inputdir + "input_fit_32_860_kaon_su_meson_PSQ0_jack.xml")
tree.write(filename)
