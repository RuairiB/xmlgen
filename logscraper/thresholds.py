import xml.etree.cElementTree as ET
import os
from glob import glob
from logutils import *

# inputdir = "/latticeQCD/raid6/ruairi/freeparticle_energies/thresholds"

def supers(inputdir):
    # Make sure all logfiles have .log extension (or start with log_ -- might be better to avoid bash logs)
    logfiles = [y for x in os.walk(inputdir) for y in glob(os.path.join(x[0], 'log_*'))]

    particles = []

    for xmlin in logfiles:
        tree = ET.parse(xmlin)
        root = tree.getroot()
        for a in root.iter("MCBinsInfo"):
            ensemble = a.find("MCEnsembleInfo").text

        if not ensemble:
            print("you need to echo the XML to find ensemble info")
            sys.exit()

        for x in root.iter("DoObsFunction"):
            obstype = x.find("Type")

            if obstype.text == "LinearSuperposition":
                temp = linsuperlog()
                temp.ensemble = ensemble

                resultinfo = x.find("ResultInfo")
                mcobs = resultinfo.find("MCObservable")
                temp.resultstr = mcobs.find("Info").text

                mcest = x.find("MCEstimate")
                temp.energy = mcest.find("FullEstimate").text
                temp.energyerr = mcest.find("SymmetricError").text
                temp.sampling = mcest.find("ResamplingMode").text


                temp.sigfigs(2)
                temp.numparticles()
                temp.stripindex()
                temp.findmom(temp.numpart)
                temp.findflav(temp.numpart)
                temp.texensemble()
                # temp.texresultstr(temp.numpart)
                temp.texthreshstr(temp.numpart)

                particles.append(temp)


            elif obstype.text == "Ratio":
                temp = particles[-1]

                resultinfo = x.find("ResultInfo")
                mcobs = resultinfo.find("MCObservable")
                temp.ratio_str = mcobs.find("Info").text

                mcest = x.find("MCEstimate")
                temp.energyratio = mcest.find("FullEstimate").text
                temp.energyratioerr = mcest.find("SymmetricError").text

                temp.sigfigs(2)
                temp.stripindex()

                particles[-1] = temp
            else:
                print("can't find ratio for " + particles[-1].resultstr + ". Or it's some other sort of DoObs I don't know.")

    # print(len(particles))

    # Loop over particles and write tex-table function
    particles.sort(key=lambda k: (k.numpart, k.psq1, k.flav1, k.psq2, k.flav2, k.psq3, k.flav3, k.psq4, k.flav4))
    # for x in particles:
    #     print(x.flav1 + x.psq1 + " " + x.flav2 + x.psq2 + " " + x.flav3 + x.psq3 + " " + x.flav4 + x.psq4)

    # Read/parse threshold files and store each threshold

    return particles
    
if __name__ == "__main__":
    junk = supers("/latticeQCD/raid6/ruairi/freeparticle_energies/thresholds")
    
