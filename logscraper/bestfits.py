import xml.etree.cElementTree as ET
import os
from glob import glob
from logutils import *

# inputdir = "/home/ruairi/research/freeparticle_energies/SH_fits"

def bestfits(inputdir):
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
    # fits.sort(key=lambda k: k.psq)

    # Separate by ensemble
    fit32 = []
    fit24 = []

    for x in fits:
        if "32" in x.ensemble:
            fit32.append(x)
        elif "24" in x.ensemble:
            fit24.append(x)

    # Separate by flavour
    kaon32 = []
    pion32 = []
    eta32 = []
    nucleon32 = []

    for x in fit32:
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

    for x in fit24:
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

    best = []
    for psq in ["0", "1", "2", "3", "4"]:
        for samp in [("Bootstrap","boot"), ("Jackknife","jack")]:
            best.append(bestfit(kaon32, psq, samp[0]))
            best.append(bestfit(kaon24, psq, samp[0]))

            best.append(bestfit(pion32, psq, samp[0]))
            best.append(bestfit(pion24, psq, samp[0]))

            if psq != "4":
                best.append(bestfit(eta32, psq, samp[0]))
                best.append(bestfit(eta24, psq, samp[0]))

            best.append(bestfit(nucleon32, psq, samp[0]))
            best.append(bestfit(nucleon24, psq, samp[0]))


    best.sort(key=lambda k: (k.ensemble, k.flav, k.psq))
    for i in best:
        destination = "/home/ruairi/research/freeparticle_energies/notes/plots/" + i.flav + i.plotlocation.split(i.flav)[2]
        if destination.endswith('.pdf'):
            destination = destination[:-4]
        texfig(i.plotlocation, destination, i)

    return best


if __name__ == "__main__":
    junk = bestfits("/home/ruairi/research/freeparticle_energies/SH_fits")
