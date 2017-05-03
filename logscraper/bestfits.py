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

                timeseps = str(fitparams.find("TimeSeparations").text)
                timeseps = timeseps.split()
                temp.tmin = str(min(int(t) for t in timeseps))
                temp.tmax = str(max(int(t) for t in timeseps))
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


    best = []
    # for psq in ["0", "1", "2", "3", "4"]:
    #     for samp in [("Bootstrap","boot"), ("Jackknife","jack")]:
    #         for flav in ["kaon", "pion", "eta", "nucleon"]:
    #             x = bestfit(fit32, flav, psq, samp[0])
    #             y = bestfit(fit24, flav, psq, samp[0])
    #             if x:
    #                 best.append(x)
    #             if y:
    #                 best.append(y)

    print("This is unfinished, see logutils:bestfit()")
    best.sort(key=lambda k: (k.ensemble, k.flav, k.psq))
    for i in fits:
        destination = "/home/ruairi/research/freeparticle_energies/notes/plots/" + i.flav + i.plotlocation.split(i.flav)[2]
        if destination.endswith('.pdf'):
            destination = destination[:-4]
        texfig(i.plotlocation, destination, i)
        # print(destination)

    return best


if __name__ == "__main__":
    junk = bestfits("/home/ruairi/research/freeparticle_energies/SH_fits")
