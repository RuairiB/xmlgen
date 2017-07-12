import xml.etree.cElementTree as ET
import os
import sys
sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/"))
from utils import *
from init import *
from tasks import *

corr_paths = ["/latticeQCD/raid8/laph/clover_s32_t256_ud860_s743/special/su_mesons/",
              "/latticeQCD/raid6/ruairi/freeparticle_energies/mom_averaging/avgbins/avgcorr_32_860_du_mesons_PSQ2",
              "/latticeQCD/raid6/ruairi/freeparticle_energies/mom_averaging/avgbins/avgcorr_32_860_su_mesons_PSQ2",
              "/latticeQCD/raid6/ruairi/freeparticle_energies/mom_averaging/avgbins/avgcorr_32_860_uu_mesons_PSQ2",
              "/latticeQCD/raid6/ruairi/freeparticle_energies/irrep_averaging/avgbins/irrepavg_32_860_uud_baryons_PSQ2"]
corr_types = ["BLCorr", "bins", "bins", "bins", "bins"]
proj_name = "doublefit32_PSQ2_boot"
inputdir = "/latticeQCD/raid6/ruairi/freeparticle_energies/ratio_comparison/"
logfile = inputdir + "log_doublefit32_PSQ2_boot.log"

root = ET.Element("SigMonD")
tree = ET.ElementTree(root)

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")

# Usage:
# initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type)

initialize(init, corr_paths, proj_name, logfile, "Bootstrap", "32_860", corr_types)

energies = []

# Fitting
tsse = "TimeSymSingleExponential"
tsseC = "TimeSymSingleExponentialPlusConstant"
tste = "TimeSymTwoExponential"
tsteC = "TimeSymTwoExponentialPlusConstant"
tsgs = "TimeSymGeomSeriesExponential"

refop = "kaon P=(0,0,0) A1u_1 SS_0"
dofit(tasks, refop, "REF1", 4, 35, tsgs, "LMDer", inputdir + "fits/kaon32_REF_PSQ0_tsgs_tmin" + str(4) + "tmax" + str(35) + "_boot.agr", 0, energies, "none", "Bootstrap")

Eref = "E1_REF1_4_35P0tsgs"


# Tasks
# dodoublefit(tasks, op1, op2, fitname1, fitname2, tmin1, tmax1, tmin2, tmax2, fitfn1, fitfn2, minimizer, plotfile, psq1, psq2, ratio_name, energies, sampling, exclude1="none", exclude2="none", pivot="none", level="none")

op = "isotriplet P=(0,1,1) A2m_1 SS_0"
refop = "kaon P=(0,0,0) A1u_1 SS_0"
plotfile = inputdir + "fits/pion32_PSQ2_doublefit_boot.agr"
dodoublefit(tasks, op, refop, "pion", "KrefP", 4, 35, 4, 35, tsgs, tsgs, "LMDer", plotfile, 2, 0, "pion32_Kref_P2", energies, "Bootstrap", exclude1="none", exclude2="none", pivot="none", level="none")
dofit(tasks, op, "pion1", 4, 35, tsgs, "LMDer", inputdir + "fits/pion32_onefit_PSQ2_tsgs_tmin" + str(4) + "tmax" + str(35) + "_boot.agr", 2, energies, Eref, "Bootstrap")


op = "isosinglet P=(0,1,1) A2p_1 SS_0"
refop = "kaon P=(0,0,0) A1u_1 SS_0"
plotfile = inputdir + "fits/eta32_PSQ2_doublefit_boot.agr"
dodoublefit(tasks, op, refop, "eta", "KrefE", 17, 25, 4, 35, tsseC, tsgs, "LMDer", plotfile, 2, 0, "eta32_Kref_P2", energies, "Bootstrap", "16", exclude2="none", pivot="none", level="none")
dofit(tasks, op, "eta1", 17, 25, tsseC, "LMDer", inputdir + "fits/eta32_onefit_PSQ2_tsseC_tmin" + str(17) + "tmax" + str(25) + "_boot.agr", 2, energies, Eref, "Bootstrap", "16")


op = "isodoublet P=(0,1,1) G_1 SS_0"
refop = "kaon P=(0,0,0) A1u_1 SS_0"
plotfile = inputdir + "fits/nucleon32_PSQ2_doublefit_boot.agr"
dodoublefit(tasks, op, refop, "nucleon", "KrefN", 3, 25, 4, 35, tsgs, tsgs, "LMDer", plotfile, 2, 0, "nucleon32_Kref_P2", energies, "Bootstrap", exclude1="none", exclude2="none", pivot="none", level="none")
dofit(tasks, op, "nucl1", 3, 25, tsgs, "LMDer", inputdir + "fits/nucleon32_onefit_PSQ2_tsgs_tmin" + str(3) + "tmax" + str(25) + "_boot.agr", 2, energies, Eref, "Bootstrap")


op = "isodoublet P=(0,1,1) A2_1 SS_0"
refop = "kaon P=(0,0,0) A1u_1 SS_0"
plotfile = inputdir + "fits/kaon32_PSQ2_doublefit_boot.agr"
dodoublefit(tasks, op, refop, "kaon", "KrefK", 5, 35, 4, 35, tsgs, tsgs, "LMDer", plotfile, 2, 0, "kaon32_Kref_P2", energies, "Bootstrap", exclude1="none", exclude2="none", pivot="none", level="none")
dofit(tasks, op, "kaon1", 5, 35, tsgs, "LMDer", inputdir + "fits/kaon32_onefit_PSQ2_tsgs_tmin" + str(5) + "tmax" + str(35) + "_boot.agr", 2, energies, Eref, "Bootstrap")


indent(root)
filename = str(inputdir + "input_doublefit32_PSQ2_boot.xml")
tree.write(filename)
