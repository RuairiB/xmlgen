import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/home/ruairi/research/phi_rho/working/rotated_matrices/rotcorr_single_phi_rho_P1_2_2_4_jack"]

proj_name = "phi_rho_fit_PSQ1_jack"
inputdir = "/home/ruairi/research/phi_rho/working/"
logfile = inputdir + "log_fit_PSQ1_jack.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_paths, proj_name, logfile, "Jackknife", "phi_rho", "bins", False)

energies = []

# Fitting
fit_types = []
fit_types.append("TimeSymSingleExponential")
fit_types.append("TimeSymSingleExponentialPlusConstant")
fit_types.append("TimeSymTwoExponential")
fit_types.append("TimeSymTwoExponentialPlusConstant")
fit_types.append("TimeSymGeomSeriesExponential")

operator0 = "isosinglet P=(0,0,1) A1g_1 rotop_P1 "
psq = "1"

# Tasks
# def dofit(tasks, optype, operator, fitname, tmin, tmax, fitfn, minimizer, plotfile, psq, energies, refenergy, sampling="Jackknife"):

#Time symmetric single exponential
level = 0

while level < 6:
    for fitfn in fit_types:
        tmin = 0
        tmax = 15
        while tmax > 5:
            while tmin < (tmax - 2):
                dofit(tasks, "GenIrreducible", operator0 + str(level), "phirho" + str(level), str(tmin), str(tmax), fitfn, "LMDer", inputdir + "fits/PSQ1/phi_rho_PSQ" + psq + "_" + shortform(fitfn) + "_tmin" + str(tmin) + "tmax" + str(tmax) + "level" + str(level) + "_jack.agr", psq, energies, "none", "Jackknife")
                tmin += 1
            tmax -= 1
            tmin = 0
            
    level += 1

    
writesamplings(tasks, energies, inputdir + "energies/phi_rho_PSQ1_jack", sampling="Jackknife")
    
indent(root)
filename = str(inputdir + "input_phi_rho_fit_PSQ1_jack.xml")
tree.write(filename)
