import xml.etree.cElementTree as ET
import os
from glob import glob
from logutils import *

inputdir = "/latticeQCD/raid6/ruairi/freeparticle_energies/SH_fits"

# Make sure all logfiles have .log extension (or start with log_ -- might be better to avoid bash logs)
logfiles = [y for x in os.walk(inputdir) for y in glob(os.path.join(x[0], 'log_*'))]

fits = []

for xmlin in logfiles:
    tree = ET.parse(xmlin)
    root = tree.getroot()
    for a in root.iter("MCBinsInfo"):
        ensemble = a.find("MCEnsembleInfo").text

    for x in root.iter("DoFit"):
        fitparams = x.find("TemporalCorrelatorFit")
        if fitparams:
            temp = fitlog()
            temp.ensemble = ensemble
            
            if fitparams.find("BLOperatorString") != None:
                temp.opstring = str(fitparams.find("BLOperatorString").text)
            elif fitparams.find("GIOperatorString") != None:
                temp.opstring = str(fitparams.find("GIOperatorString").text)
            else:
                print("can't find operatorstring in " + xmlin)
                sys.exit()

            temp.psqfromstring()
            temp.texopstring()
            temp.texensemble()
            temp.tmin = str(fitparams.find("MinimumTimeSeparation").text)
            temp.tmax = str(fitparams.find("MaximumTimeSeparation").text)
            temp.model = str(fitparams.find("Model").text)
            
            fitresult = x.find("BestFitResult")
            if fitresult:
                temp.chisq = str(fitresult.find("ChiSquarePerDof").text)
                energyresult = fitresult.find("FitParameter0")
                mcobs = energyresult.find("MCObservable")
                temp.fitname = mcobs.find("Info").text
                mcest = energyresult.find("MCEstimate")
                temp.sampling = mcest.find("ResamplingMode").text
                temp.fitenergy = mcest.find("FullEstimate").text
                temp.fiterr = mcest.find("SymmetricError").text
                
                temp.sigfigs(2)
                temp.stripindex()
                temp.findflav()
                temp.findplot()
                # Only add to list of fit results if good fit
                fits.append(temp)

# Sort list by P^2
fits.sort(key=lambda k: k.psq)

# Separate by ensemble
fit32 = []
fit24 = []

for x in fits:
    if "32" in x.ensemble:
        fit32.append(x)
    if "24" in x.ensemble:
        fit24.append(x)

# Separate by flavour
kaon32 = []
pion32 = []
eta32 = []
nucleon32 = []

for x in fit32:
    if any(flav in x.opstring for flav in ["kaon", "A1_", "A2_"]):
        kaon32.append(x)
    elif any(flav in x.opstring for flav in ["G1g_", "G1_", "G_"]):
        nucleon32.append(x)
    elif any(flav in x.opstring for flav in ["pion", "isotriplet"]):
        pion32.append(x)
    elif any(flav in x.opstring for flav in ["eta", "isosinglet"]):
        eta32.append(x)
    else:
        print("Unknown operator32 flavour")
        sys.exit()

kaon24 = []
pion24 = []
eta24 = []
nucleon24 = []

for x in fit24:
    if any(flav in x.opstring for flav in ["kaon", "A1_", "A2_"]):
        kaon24.append(x)
    elif any(flav in x.opstring for flav in ["G1g_", "G1_", "G_"]):
        nucleon24.append(x)
    elif any(flav in x.opstring for flav in ["pion", "isotriplet"]):
        pion24.append(x)
    elif any(flav in x.opstring for flav in ["eta", "isosinglet"]):
        eta24.append(x)
    else:
        print("Unknown operator24 flavour")
        sys.exit()


# # shit out latex tables
for psq in ["0", "1", "2", "3", "4"]:
    for samp in [("Bootstrap","boot"), ("Jackknife","jack")]:
        textable_fits(kaon24, psq, samp[0], "/latticeQCD/raid6/ruairi/freeparticle_energies/notes/tables/kaon24_PSQ" + psq + "_" + samp[1])
        textable_fits(kaon32, psq, samp[0], "/latticeQCD/raid6/ruairi/freeparticle_energies/notes/tables/kaon32_PSQ" + psq + "_" + samp[1])

        textable_fits(pion24, psq, samp[0], "/latticeQCD/raid6/ruairi/freeparticle_energies/notes/tables/pion24_PSQ" + psq + "_" + samp[1])
        textable_fits(pion32, psq, samp[0], "/latticeQCD/raid6/ruairi/freeparticle_energies/notes/tables/pion32_PSQ" + psq + "_" + samp[1])

        textable_fits(nucleon24, psq, samp[0], "/latticeQCD/raid6/ruairi/freeparticle_energies/notes/tables/nucleon24_PSQ" + psq + "_" + samp[1])
        textable_fits(nucleon32, psq, samp[0], "/latticeQCD/raid6/ruairi/freeparticle_energies/notes/tables/nucleon32_PSQ" + psq + "_" + samp[1])

        textable_fits(eta24, psq, samp[0], "/latticeQCD/raid6/ruairi/freeparticle_energies/notes/tables/eta24_PSQ" + psq + "_" + samp[1])
        textable_fits(eta32, psq, samp[0], "/latticeQCD/raid6/ruairi/freeparticle_energies/notes/tables/eta32_PSQ" + psq + "_" + samp[1])
