import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/home/ruairi/research/correlator_data/clover_s24_t128_ud840_s743/special/uu_mesons/"]
proj_name = "fit_24_840_eta_uu_meson_PSQ0"
inputdir = "/home/ruairi/research/freeparticle_energies/SH_fits/24^3/eta/"
logfile = inputdir + "log_fit_24_840_eta_uu_meson_PSQ0_boot.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "24_840", "BLCorr")

energies = []

# Fitting
tsse = "TimeSymSingleExponential"
tsseC = "TimeSymSingleExponentialPlusConstant"
tste = "TimeSymTwoExponential"
tsteC = "TimeSymTwoExponentialPlusConstant"
tsgs = "TimeSymGeomSeriesExponential"

# Tasks
# dofit(tasks, optype, operator, tmin, tmax, fitfn, plotfile, psq, energies, "E1_ref_5_35P0tsgs", sampling="Bootstrap")
# writesamplings(tasks, energies, energyfile, sampling="Bootstrap")

readsamplings(tasks, "/home/ruairi/research/freeparticle_energies/refenergies/kaon24_PSQ0_reference_bins_boot", "Bootstrap", ["E1_ref_5_35P0tsgs"])
#Time symmetric single exponential
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 6):
        dofit(tasks, "BasicLaph", "eta P=(0,0,0) A1up_1 SS_0", "eta", str(tmin), str(tmax), tsseC, "Minuit2", inputdir + "fits/PSQ0/eta_24_840_PSQ0_tsseC_tmin" + str(tmin) + "tmax" + str(tmax) + "_boot.agr", "0", energies, "E1_ref_5_35P0tsgs", "Bootstrap")
        tmin+=1
    tmax-=1
    tmin=3

#Time symmetric two exponential    
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 15):
        dofit(tasks, "BasicLaph", "eta P=(0,0,0) A1up_1 SS_0", "eta", str(tmin), str(tmax), tsteC, "Minuit2", inputdir + "fits/PSQ0/eta_24_840_PSQ0_tsteC_tmin" + str(tmin) + "tmax" + str(tmax) + "_boot.agr", "0", energies, "E1_ref_5_35P0tsgs", "Bootstrap")
        tmin+=1
    tmax-=1
    tmin=3

#Time symmetric geometric series    
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 15):
        dofit(tasks, "BasicLaph", "eta P=(0,0,0) A1up_1 SS_0", "eta", str(tmin), str(tmax), tsgs, "Minuit2", inputdir + "fits/PSQ0/eta_24_840_PSQ0_tsgs_tmin" + str(tmin) + "tmax" + str(tmax) + "_boot.agr", "0", energies, "E1_ref_5_35P0tsgs", "Bootstrap")
        tmin+=1
    tmax-=1
    tmin=3

    
writesamplings(tasks, energies, inputdir + "energies/eta_24_840_PSQ0_boot", sampling="Bootstrap")
    
indent(root)
filename = str(inputdir + "input_fit_24_840_eta_uu_meson_PSQ0_boot.xml")
tree.write(filename)
