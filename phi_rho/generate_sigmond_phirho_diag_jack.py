import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/"))
from utils import *
from init import *
from tasks import *

sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/logscraper/"))
from logutils import *
from bestfits import *

corr_paths = ["/home/ruairi/research/correlator_data/phi_rho/s32_t48/phirho_s32_t48_mp0150_mr0350_lm0050_0300.bins"]

proj_name = "phi_rho_diag_jack"
inputdir = "/home/ruairi/research/phi_rho/working/"
logfile = inputdir + "log_diag_jack.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_paths, proj_name, logfile, "Jackknife", "phi_rho", "bins")

# Tasks
# rotatematrix(tasks, piv_type, oplist, herm, vev, rotop, piv_name, tmin, tmax, tnorm, tmet, tdiag, piv_file, rotcorr_file, plot_sampling, effenergytype, plotstub):
oplistP0 = ["isosinglet P=(0,0,0) A1g_1 Phi(0)",
            "isosinglet P=(0,0,0) A1g_1 Phi(0)Phi(0)",
            "isosinglet P=(0,0,0) A1g_1 Phi(1)Phi(1)",
            "isosinglet P=(0,0,0) A1g_1 Phi(2)Phi(2)",
            "isosinglet P=(0,0,0) A1g_1 Phi(3)Phi(3)",
            "isosinglet P=(0,0,0) A1g_1 Phi(4)Phi(4)",
            "isosinglet P=(0,0,0) A1g_1 Rho(0)"]

rotopP0 = "isosinglet P=(0,0,0) A1g_1 rotop_P0"

oplistP1 = ["isosinglet P=(0,0,1) A1_1 Phi(1)",
            "isosinglet P=(0,0,1) A1_1 Phi(1)Phi(0)",
            "isosinglet P=(0,0,1) A1_1 Phi(2)Phi(1)",
            "isosinglet P=(0,0,1) A1_1 Phi(3)Phi(2)",
            "isosinglet P=(0,0,1) A1_1 Phi(4)Phi(1)",
            "isosinglet P=(0,0,1) A1_1 Rho(1)"]

rotopP1 = "isosinglet P=(0,0,1) A1g_1 rotop_P1"

rotatematrix(tasks, "SinglePivot", oplistP0, True, True, rotopP0, "pivotsingle_phi_rho_P0_jack", "0", "15", "0", "0", "1", inputdir + "pivots/pivotsingle_phi_rho_P0_0_0_1_jack", inputdir + "rotated_matrices/rotcorr_single_phi_rho_P0_0_0_1_jack", "Jackknife", "TimeSymmetric", inputdir + "plots/phi_rho_singlepiv_P0_0_0_1_jack_level")

rotatematrix(tasks, "SinglePivot", oplistP1, True, False, rotopP1, "pivotsingle_phi_rho_P1_jack", "0", "15", "0", "0", "1", inputdir + "pivots/pivotsingle_phi_rho_P1_0_0_1_jack", inputdir + "rotated_matrices/rotcorr_single_phi_rho_P1_0_0_1_jack", "Jackknife", "TimeSymmetric", inputdir + "plots/phi_rho_singlepiv_P1_0_0_1_jack_level")

# rotatematrix(tasks, "RollingPivot", oplistP0, True, True, rotopP0, "pivotrolling_phi_rho_P0_jack", "0", "15", "0", "0", "1", inputdir + "pivots/pivotrolling_phi_rho_P0_0_0_1_jack", inputdir + "rotated_matrices/rotcorr_rolling_phi_rho_P0_0_0_1_jack", "Jackknife", "TimeSymmetric", inputdir + "plots/phi_rho_rollingpiv_P0_0_0_1_jack_level")

# rotatematrix(tasks, "RollingPivot", oplistP1, True, False, rotopP1, "pivotrolling_phi_rho_P1_jack", "0", "15", "0", "0", "1", inputdir + "pivots/pivotrolling_phi_rho_P1_0_0_1_jack", inputdir + "rotated_matrices/rotcorr_rolling_phi_rho_P1_0_0_1_jack", "Jackknife", "TimeSymmetric", inputdir + "plots/phi_rho_rollingpiv_P1_0_0_1_jack_level")

#writesamplings(tasks, energies, inputdir + "samplings/32_860_PSQ0_jack", sampling="Jackknife")
    
indent(root)
filename = str(inputdir + "input_phi_rho_diag_jack.xml")
tree.write(filename)
