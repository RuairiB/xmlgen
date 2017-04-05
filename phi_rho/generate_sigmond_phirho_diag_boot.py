import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/"))
from utils import *
from init import *
from tasks import *

sys.path.append(os.path.abspath("/home/ruairi/research/xmlgen/logscraper/"))
from logutils import *
from bestfits import *

corr_paths = ["/home/ruairi/research/correlator_data/phi_rho/s32_t48/phirho_s32_t48_mp0150_mr0350_lm0050_0300.bins"]

proj_name = "phi_rho_diag_boot"
inputdir = "/home/ruairi/research/phi_rho/working/"
logfile = inputdir + "log_diag_boot.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "phi_rho", "bins")

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

rotatematrix(tasks, "SinglePivot", oplistP0, True, True, rotopP0, "pivotsingle_phi_rho_P0_boot", "0", "15", "2", "2", "4", inputdir + "pivots/pivotsingle_phi_rho_P0_2_2_4_boot", inputdir + "rotated_matrices/rotcorr_single_phi_rho_P0_2_2_4_boot", "Bootstrap", "TimeSymmetric", inputdir + "plots/phi_rho_singlepiv_P0_2_2_4_boot_level")

rotatematrix(tasks, "SinglePivot", oplistP1, True, False, rotopP1, "pivotsingle_phi_rho_P1_boot", "0", "15", "2", "2", "4", inputdir + "pivots/pivotsingle_phi_rho_P1_2_2_4_boot", inputdir + "rotated_matrices/rotcorr_single_phi_rho_P1_2_2_4_boot", "Bootstrap", "TimeSymmetric", inputdir + "plots/phi_rho_singlepiv_P1_2_2_4_boot_level")

# rotatematrix(tasks, "RollingPivot", oplistP0, True, True, rotopP0, "pivotrolling_phi_rho_P0_boot", "0", "15", "2", "2", "4", inputdir + "pivots/pivotrolling_phi_rho_P0_2_2_4_boot", inputdir + "rotated_matrices/rotcorr_rolling_phi_rho_P0_2_2_4_boot", "Bootstrap", "TimeSymmetric", inputdir + "plots/phi_rho_rollingpiv_P0_2_2_4_boot_level")

# rotatematrix(tasks, "RollingPivot", oplistP1, True, False, rotopP1, "pivotrolling_phi_rho_P1_boot", "0", "15", "2", "2", "4", inputdir + "pivots/pivotrolling_phi_rho_P1_2_2_4_boot", inputdir + "rotated_matrices/rotcorr_rolling_phi_rho_P1_2_2_4_boot", "Bootstrap", "TimeSymmetric", inputdir + "plots/phi_rho_rollingpiv_P1_2_2_4_boot_level")

#writesamplings(tasks, energies, inputdir + "samplings/32_860_PSQ0_boot", sampling="Bootstrap")
    
indent(root)
filename = str(inputdir + "input_phi_rho_diag_boot.xml")
tree.write(filename)
