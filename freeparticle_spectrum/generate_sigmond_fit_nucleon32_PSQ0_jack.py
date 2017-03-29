import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/home/ruairi/research/freeparticle_energies/irrep_averaging/avgbins/irrepavg_32_860_uud_baryons_PSQ0"]
proj_name = "fit_32_860_nucleon_uud_baryon_PSQ0"
inputdir = "/home/ruairi/research/freeparticle_energies/SH_fits/32^3/nucleon/"
logfile = inputdir + "log_fit_32_860_nucleon_uud_baryon_PSQ0_jack.log"

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

operator = "isodoublet P=(0,0,0) G1g_1 SS_0"
psq = "0"

# Tasks
# dofit(tasks, optype, operator, tmin, tmax, fitfn, plotfile, psq, energies, "E1_tmin8tmax34P0tsgs", sampling="Jackknife")
# writesamplings(tasks, energies, energyfile, sampling="Jackknife")

readsamplings(tasks, "/home/ruairi/research/freeparticle_energies/refenergies/kaon32_PSQ0_reference_bins_jack", "Jackknife", ["E1_tmin8tmax34P0tsgs"])
#Time symmetric single exponential
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 6):
        dofit(tasks, "GenIrreducible", operator, "nucleon", str(tmin), str(tmax), tsse, "Minuit2", inputdir + "fits/PSQ0/nucleon_32_860_PSQ0_tsse_tmin" + str(tmin) + "tmax" + str(tmax) + "_jack.agr", psq, energies, "E1_tmin8tmax34P0tsgs", "Jackknife")
        tmin+=1
    tmax-=1
    tmin=3

#Time symmetric two exponential    
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 15):
        dofit(tasks, "GenIrreducible", operator, "nucleon", str(tmin), str(tmax), tste, "Minuit2", inputdir + "fits/PSQ0/nucleon_32_860_PSQ0_tste_tmin" + str(tmin) + "tmax" + str(tmax) + "_jack.agr", psq, energies, "E1_tmin8tmax34P0tsgs", "Jackknife")
        tmin+=1
    tmax-=1
    tmin=3

#Time symmetric geometric series    
tmin = 3
tmax = 25

while tmax > 20:
    while tmin < (tmax - 15):
        dofit(tasks, "GenIrreducible", operator, "nucleon", str(tmin), str(tmax), tsgs, "Minuit2", inputdir + "fits/PSQ0/nucleon_32_860_PSQ0_tsgs_tmin" + str(tmin) + "tmax" + str(tmax) + "_jack.agr", psq, energies, "E1_tmin8tmax34P0tsgs", "Jackknife")
        tmin+=1
    tmax-=1
    tmin=3

    
writesamplings(tasks, energies, inputdir + "energies/nucleon_32_860_PSQ0_jack", sampling="Jackknife")
    
indent(root)
filename = str(inputdir + "input_fit_32_860_nucleon_uud_baryon_PSQ0_jack.xml")
tree.write(filename)