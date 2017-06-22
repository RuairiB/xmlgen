import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/home/ruairi/research/freeparticle_energies/mom_averaging/avgbins/avgcorr_32_860_su_mesons_PSQ5"]
proj_name = "fit_32_860_kaon_su_meson_PSQ5"
inputdir = "/home/ruairi/research/freeparticle_energies/SH_fits/32^3/kaon/"
logfile = inputdir + "log_fit_32_860_kaon_su_meson_PSQ5_boot.log"

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

operator = "isodoublet P=(1,2,0) A2_1 SS_0"
psq = "5"

# Tasks
# dofit(tasks, optype, operator, tmin, tmax, fitfn, plotfile, psq, energies, "E1_kaon_4_35P0tsgs", sampling="Bootstrap")
# writesamplings(tasks, energies, energyfile, sampling="Bootstrap")

readsamplings(tasks, "/home/ruairi/research/freeparticle_energies/refenergies/kaon32_PSQ0_reference_bins_boot", "Bootstrap", ["E1_kaon_4_35P0tsgs"])

tmin = 3
tmax = 38

while tmax > 30:
    while tmin < 10:
        dofit(tasks, operator, "kaon", str(tmin), str(tmax), tsgs, "LMDer", inputdir + "fits/PSQ5/kaon_32_860_PSQ5_tsgs_tmin" + str(tmin) + "tmax" + str(tmax) + "_boot.agr", psq, energies, "E1_kaon_4_35P0tsgs", "Bootstrap")
        tmin+=1
    tmax-=1
    tmin=3
    
writesamplings(tasks, energies, inputdir + "energies/kaon_32_860_PSQ5_boot", sampling="Bootstrap")
    
indent(root)
filename = str(inputdir + "input_fit_32_860_kaon_su_meson_PSQ5_boot.xml")
tree.write(filename)