import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/home/ruairi/research/freeparticle_energies/mom_averaging/avgbins/avgcorr_32_860_du_mesons_PSQ4"]
proj_name = "fit_32_860_pion_du_meson_PSQ4"
inputdir = "/home/ruairi/research/freeparticle_energies/SH_fits/32^3/pion/"
logfile = inputdir + "log_fit_32_860_pion_du_meson_PSQ4_jack.log"

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

operator = "isotriplet P=(0,0,2) A2m_1 SS_1"
psq = "4"

# Tasks
# dofit(tasks, optype, operator, tmin, tmax, fitfn, plotfile, psq, energies, "E1_kaon_4_35P0tsgs", sampling="Jackknife")
# writesamplings(tasks, energies, energyfile, sampling="Jackknife")

readsamplings(tasks, "/home/ruairi/research/freeparticle_energies/refenergies/kaon32_PSQ0_reference_bins_jack", "Jackknife", ["E1_kaon_4_35P0tsgs"])
#Time symmetric single exponential
tmin = 3
tmax = 35

while tmax > 30:
    while tmin < (tmax - 6):
        dofit(tasks, operator, "pion", str(tmin), str(tmax), tsse, "LMDer", inputdir + "fits/PSQ4/pion_32_860_PSQ4_tsse_tmin" + str(tmin) + "tmax" + str(tmax) + "_jack.agr", psq, energies, "E1_kaon_4_35P0tsgs", "Jackknife")
        tmin+=1
    tmax-=1
    tmin=3

#Time symmetric two exponential    
tmin = 3
tmax = 35

while tmax > 30:
    while tmin < (tmax - 15):
        dofit(tasks, operator, "pion", str(tmin), str(tmax), tste, "LMDer", inputdir + "fits/PSQ4/pion_32_860_PSQ4_tste_tmin" + str(tmin) + "tmax" + str(tmax) + "_jack.agr", psq, energies, "E1_kaon_4_35P0tsgs", "Jackknife")
        tmin+=1
    tmax-=1
    tmin=3

#Time symmetric geometric series    
tmin = 3
tmax = 35

while tmax > 30:
    while tmin < (tmax - 15):
        dofit(tasks, operator, "pion", str(tmin), str(tmax), tsgs, "LMDer", inputdir + "fits/PSQ4/pion_32_860_PSQ4_tsgs_tmin" + str(tmin) + "tmax" + str(tmax) + "_jack.agr", psq, energies, "E1_kaon_4_35P0tsgs", "Jackknife")
        tmin+=1
    tmax-=1
    tmin=3

    
writesamplings(tasks, energies, inputdir + "energies/pion_32_860_PSQ4_jack", sampling="Jackknife")
    
indent(root)
filename = str(inputdir + "input_fit_32_860_pion_du_meson_PSQ4_jack.xml")
tree.write(filename)
