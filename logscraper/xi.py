import xml.etree.cElementTree as ET
import sys
import os
from glob import glob
from logutils import *

# inputdir = "/latticeQCD/raid6/ruairi/freeparticle_energies/SH_fits"

def xifits(inputdir):
    # Make sure all logfiles have .log extension (or start with log_ -- might be better to avoid bash logs)
    logfiles = [y for x in os.walk(inputdir) for y in glob(os.path.join(x[0], 'log_*'))]

    fits = []

    for xmlin in logfiles:
        tree = ET.parse(xmlin)
        root = tree.getroot()
        ensemble = None
        for a in root.iter("MCBinsInfo"):
            ensemble = a.find("MCEnsembleInfo").text

        if not ensemble:
            if "32" in xmlin:
                ensemble = "clover_s32_t256_ud860_s743"
            elif "24" in xmlin:
                ensemble = "clover_s24_t128_ud840_s743"
            else:
                print("can't find the ensemble info")
                sys.exit()

        for x in root.iter("DoFit"):
            fitparams = x.find("AnisotropyFromDispersionFit")
            if fitparams:
                temp = fitlog()
                temp.ensemble = ensemble

                anisotropy = fitparams.find("Anisotropy")
                xiobs = anisotropy.find("MCObservable")
                temp.xistring = str(xiobs.find("Info").text)

                # temp.stripxi()
                temp.texensemble()

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
                    temp.findflav(True)
                    # temp.findplot()
                    # Only add to list of fit results if good fit?
                    fits.append(temp)

    # Sort list by flav
    fits.sort(key=lambda k: k.flav)

    return fits


if __name__ == "__main__":
    junk = xifits("/latticeQCD/raid6/ruairi/freeparticle_energies/aspect_ratio")

    junk32 = []
    junk24 = []
    for x in junk:
        if "32" in x.ensemble:
            junk32.append(x)
        elif "24" in x.ensemble:
            junk24.append(x)
        else:
            print("fuck you. ensemble")
            sys.exit()


    # Separate by flavour
    kaon32 = []
    pion32 = []
    eta32 = []
    nucleon32 = []

    for x in junk32:
        if x.flav == "kaon":
            kaon32.append(x)
        elif x.flav == "nucleon":
            nucleon32.append(x)
        elif x.flav == "pion":
            pion32.append(x)
        elif x.flav == "eta":
            eta32.append(x)
        else:
            print("Unknown operator32 flavour")
            sys.exit()

    kaon24 = []
    pion24 = []
    eta24 = []
    nucleon24 = []

    for x in junk24:
        if x.flav == "kaon":
            kaon24.append(x)
        elif x.flav == "nucleon":
            nucleon24.append(x)
        elif x.flav == "pion":
            pion24.append(x)
        elif x.flav == "eta":
            eta24.append(x)
        else:
            print("Unknown operator24 flavour")
            sys.exit()


    print(min(kaon32, key=lambda x:abs(float(x.chisq_full) - 1)).xistring)
    print(min(pion32, key=lambda x:abs(float(x.chisq_full) - 1)).xistring)
    print(min(nucleon32, key=lambda x:abs(float(x.chisq_full) - 1)).xistring)
    print(min(eta32, key=lambda x:abs(float(x.chisq_full) - 1)).xistring)

    print(min(kaon24, key=lambda x:abs(float(x.chisq_full) - 1)).xistring)
    print(min(pion24, key=lambda x:abs(float(x.chisq_full) - 1)).xistring)
    print(min(nucleon24, key=lambda x:abs(float(x.chisq_full) - 1)).xistring)
    print(min(eta24, key=lambda x:abs(float(x.chisq_full) - 1)).xistring)
