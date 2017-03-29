import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_path = ["/latticeQCD/raid8/laph/clover_s32_t256_ud860_s743/special/du_mesons/"]
proj_name = "fit_32_860_pion_du_meson_testing"
inputdir = "/latticeQCD/raid6/ruairi/freeparticle_energies/SH_fits/32^3/pion/"
logfile = inputdir + "log_fit_32_860_pion_du_meson_testing_jack.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_path, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_path, proj_name, logfile, "Jackknife", "32_860", "BLCorr")

energies = []

# Fitting
tsse = "TimeSymSingleExponential"
tsseC = "TimeSymSingleExponentialPlusConstant"
tste = "TimeSymTwoExponential"
tsteC = "TimeSymTwoExponentialPlusConstant"
tsgs = "TimeSymGeomSeriesExponential"

# PSQ = 0
tmin = 3
tmax = 35

dofit(tasks, "BasicLaph", "pion P=(0,0,0) A1um_1 SS_0", "pion", str(tmin), str(tmax), tste, "Minuit2", inputdir + "fits/testing/pion_32_860_testing_PSQ0_jack.agr", "0", energies, "E1_tmin8tmax34P0tsgs", "Jackknife")

# PSQ = 1
tmin = 3
tmax = 35

dofit(tasks, "BasicLaph", "pion P=(0,0,1) A2m_1 SS_1", "pion", str(tmin), str(tmax), tste, "Minuit2", inputdir + "fits/testing/pion_32_860_testing_PSQ1_jack.agr", "0", energies, "E1_tmin8tmax34P0tsgs", "Jackknife")

# PSQ = 2
tmin = 3
tmax = 35

dofit(tasks, "BasicLaph", "pion P=(0,1,1) A2m_1 SS_0", "pion", str(tmin), str(tmax), tste, "Minuit2", inputdir + "fits/testing/pion_32_860_testing_PSQ2_jack.agr", "0", energies, "E1_tmin8tmax34P0tsgs", "Jackknife")

# PSQ = 3
tmin = 3
tmax = 35

dofit(tasks, "BasicLaph", "pion P=(1,1,1) A2m_1 SS_0", "pion", str(tmin), str(tmax), tste, "Minuit2", inputdir + "fits/testing/pion_32_860_testing_PSQ3_jack.agr", "0", energies, "E1_tmin8tmax34P0tsgs", "Jackknife")

# PSQ = 4
tmin = 3
tmax = 35

dofit(tasks, "BasicLaph", "pion P=(0,0,2) A2m_1 SS_1", "pion", str(tmin), str(tmax), tste, "Minuit2", inputdir + "fits/testing/pion_32_860_testing_PSQ4_jack.agr", "0", energies, "E1_tmin8tmax34P0tsgs", "Jackknife")

writesamplings(tasks, energies, inputdir + "energies/pion_32_860_testing_jack", sampling="Jackknife")
    
indent(root)
filename = str(inputdir + "input_fit_32_860_pion_du_meson_testing_jack.xml")
tree.write(filename)
