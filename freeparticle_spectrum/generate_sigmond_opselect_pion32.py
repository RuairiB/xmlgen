import xml.etree.cElementTree as ET
import os
from utils import *
from init import *
from tasks import *

corr_path = ["/home/ruairi/research/correlator_data/clover_s32_t256_ud860_s743/special/du_mesons/"]
proj_name = "diagcorr_32_860_pion_du_meson"
inputdir = "/home/ruairi/research/freeparticle_energies/operator_selection/32^3/"
logfile = inputdir + "log_diagcorr_32_860_du_meson_pion" + ".log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_path, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_path, proj_name, logfile, "Jackknife", "32_860", "BLCorr")

# Tasks
# dofit(tasks, optype, operator, tmin, tmax, fitfn, plotfile, psq, energies, sampling="Bootstrap")
# writesamplings(tasks, energies, energyfile, sampling="Bootstrap")

ops_psq0 = getopsdef("/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_32_860_du.rb", 0)
ops_psq1 = getopsdef("/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_32_860_du.rb", 1)
ops_psq2 = getopsdef("/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_32_860_du.rb", 2)
ops_psq3 = getopsdef("/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_32_860_du.rb", 3)
ops_psq4 = getopsdef("/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_32_860_du.rb", 4)
ops_psq5 = getopsdef("/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_32_860_du.rb", 5)
ops_psq6 = getopsdef("/home/ruairi/research/freeparticle_energies/run_scripts/opdefs_32_860_du.rb", 6)

diagonalenergyplots(tasks, ops_psq0, inputdir + "plots/pion/diagcorr_32_860_du_meson_P0", "Jackknife")
diagonalenergyplots(tasks, ops_psq1, inputdir + "plots/pion/diagcorr_32_860_du_meson_P1", "Jackknife")
diagonalenergyplots(tasks, ops_psq2, inputdir + "plots/pion/diagcorr_32_860_du_meson_P2", "Jackknife")
diagonalenergyplots(tasks, ops_psq3, inputdir + "plots/pion/diagcorr_32_860_du_meson_P3", "Jackknife")
diagonalenergyplots(tasks, ops_psq4, inputdir + "plots/pion/diagcorr_32_860_du_meson_P4", "Jackknife")
diagonalenergyplots(tasks, ops_psq5, inputdir + "plots/pion/diagcorr_32_860_du_meson_P5", "Jackknife")
diagonalenergyplots(tasks, ops_psq6, inputdir + "plots/pion/diagcorr_32_860_du_meson_P6", "Jackknife")
    
indent(root)
filename = str(inputdir + "input_diagcorr_32_860_du_meson_pion.xml")
tree.write(filename)
