import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/home/ruairi/research/freeparticle_energies/mom_averaging/avgbins/avgcorr_24_840_du_mesons_PSQ6"]
proj_name = "fit_24_840_pion_du_meson_PSQ6"
inputdir = "/home/ruairi/research/freeparticle_energies/SH_fits/24^3/pion/"
logfile = inputdir + "log_fit_24_840_pion_du_meson_PSQ6_boot.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "24_840", "bins")

energies = []

# Fitting
tsse = "TimeSymSingleExponential"
tsseC = "TimeSymSingleExponentialPlusConstant"
tste = "TimeSymTwoExponential"
tsteC = "TimeSymTwoExponentialPlusConstant"
tsgs = "TimeSymGeomSeriesExponential"

operator = "isotriplet P=(1,1,2) A2m_1 SS_0"
psq = "6"

# Tasks
# dofit(tasks, optype, operator, tmin, tmax, fitfn, plotfile, psq, energies, "E1_kaon_4_35P0tsgs", sampling="Bootstrap")
# writesamplings(tasks, energies, energyfile, sampling="Bootstrap")

readsamplings(tasks, "/home/ruairi/research/freeparticle_energies/refenergies/kaon24_PSQ0_reference_bins_boot", "Bootstrap", ["E1_ref_5_35P0tsgs"])

tmin = 3
tmax = 38

while tmax > 30:
    while tmin < 10:
        dofit(tasks, operator, "pion", str(tmin), str(tmax), tsgs, "LMDer", inputdir + "fits/PSQ6/pion_24_840_PSQ6_tsgs_tmin" + str(tmin) + "tmax" + str(tmax) + "_boot.agr", psq, energies, "E1_ref_5_35P0tsgs", "Bootstrap")
        tmin+=1
    tmax-=1
    tmin=3


writesamplings(tasks, energies, inputdir + "energies/pion_24_840_PSQ6_boot", sampling="Bootstrap")
    
indent(root)
filename = str(inputdir + "input_fit_24_840_pion_du_meson_PSQ6_boot.xml")
tree.write(filename)






# #Time symmetric single exponential
# tmin = 3
# tmax = 38

# while tmax > 30:
#     while tmin < (tmax - 6):
#         dofit(tasks, operator, "pion", str(tmin), str(tmax), tsse, "LMDer", inputdir + "fits/PSQ6/pion_24_840_PSQ6_tsse_tmin" + str(tmin) + "tmax" + str(tmax) + "_boot.agr", psq, energies, "E1_kaon_4_35P0tsgs", "Bootstrap")
#         tmin+=1
#     tmax-=1
#     tmin=3

# #Time symmetric two exponential    
# tmin = 3
# tmax = 38

# while tmax > 30:
#     while tmin < (tmax - 15):
#         dofit(tasks, operator, "pion", str(tmin), str(tmax), tste, "LMDer", inputdir + "fits/PSQ6/pion_24_840_PSQ6_tste_tmin" + str(tmin) + "tmax" + str(tmax) + "_boot.agr", psq, energies, "E1_kaon_4_35P0tsgs", "Bootstrap")
#         tmin+=1
#     tmax-=1
#     tmin=3

# #Time symmetric geometric series    
# tmin = 3
# tmax = 38

# while tmax > 30:
#     while tmin < (tmax - 15):
#         dofit(tasks, operator, "pion", str(tmin), str(tmax), tsgs, "LMDer", inputdir + "fits/PSQ6/pion_24_840_PSQ6_tsgs_tmin" + str(tmin) + "tmax" + str(tmax) + "_boot.agr", psq, energies, "E1_kaon_4_35P0tsgs", "Bootstrap")
#         tmin+=1
#     tmax-=1
#     tmin=3