import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/home/ruairi/research/freeparticle_energies/mom_averaging/avgbins/avgcorr_32_860_uu_mesons_PSQ2"]
proj_name = "fit_32_860_eta_uu_meson_PSQ2"
inputdir = "/home/ruairi/research/freeparticle_energies/SH_fits/32^3/eta/"
logfile = inputdir + "log_fit_32_860_eta_uu_meson_PSQ2_jack.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_paths, proj_name, logfile, "Jackknife", "32_860", "bins")

energies = []

# Fitting
tsse = "TimeSymSingleExponential"
tsseC = "TimeSymSingleExponentialPlusConstant"
tste = "TimeSymTwoExponential"
tsteC = "TimeSymTwoExponentialPlusConstant"
tsgs = "TimeSymGeomSeriesExponential"

operator = "isosinglet P=(0,1,1) A2p_1 SS_0"
psq = "2"

# Tasks
# dofit(tasks, optype, operator, tmin, tmax, fitfn, plotfile, psq, energies, "E1_tmin8tmax34P0tsgs", sampling="Jackknife")
# writesamplings(tasks, energies, energyfile, sampling="Jackknife")

readsamplings(tasks, "/home/ruairi/research/freeparticle_energies/refenergies/kaon32_PSQ0_reference_bins_jack", "Jackknife", ["E1_tmin8tmax34P0tsgs"])
#Time symmetric single exponential
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 3):
        dofit(tasks, operator, "eta", str(tmin), str(tmax), tsse, "LMDer", inputdir + "fits/PSQ2/eta_32_860_PSQ2_tsse_tmin" + str(tmin) + "tmax" + str(tmax) + "_jack.agr", psq, energies, "E1_tmin8tmax34P0tsgs", "Jackknife")
        tmin+=1
    tmax-=1
    tmin=3

#Time symmetric two exponential    
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 10):
        dofit(tasks, operator, "eta", str(tmin), str(tmax), tste, "LMDer", inputdir + "fits/PSQ2/eta_32_860_PSQ2_tste_tmin" + str(tmin) + "tmax" + str(tmax) + "_jack.agr", psq, energies, "E1_tmin8tmax34P0tsgs", "Jackknife")
        tmin+=1
    tmax-=1
    tmin=3

#Time symmetric geometric series    
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 3):
        dofit(tasks, operator, "eta", str(tmin), str(tmax), tsseC, "LMDer", inputdir + "fits/PSQ2/eta_32_860_PSQ2_tsseC_tmin" + str(tmin) + "tmax" + str(tmax) + "_jack.agr", psq, energies, "E1_tmin8tmax34P0tsgs", "Jackknife")
        tmin+=1
    tmax-=1
    tmin=3

    
writesamplings(tasks, energies, inputdir + "energies/eta_32_860_PSQ2_jack", sampling="Jackknife")
    
indent(root)
filename = str(inputdir + "input_fit_32_860_eta_uu_meson_PSQ2_jack.xml")
tree.write(filename)
