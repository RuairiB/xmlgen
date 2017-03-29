import xml.etree.cElementTree as ET
import os
from glob import glob
from logutils import *

inputdir = "/latticeQCD/raid6/ruairi/freeparticle_energies/two_particles"

# Make sure all logfiles have .log extension (or start with log_ -- might be better to avoid bash logs)
logfiles = [y for x in os.walk(inputdir) for y in glob(os.path.join(x[0], 'log_*'))]

particles = []

for xmlin in logfiles:
    tree = ET.parse(xmlin)
    root = tree.getroot()
    for a in root.iter("MCBinsInfo"):
        ensemble = a.find("MCEnsembleInfo").text

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
            temp.stripindex()
            temp.findmom()
            temp.findflav()
            temp.calcptot()
            temp.texensemble()
            temp.texresultstr()
            
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
            print("can't find ratio for " + particles[-1].resultstr)


            
            

# Loop over particles and write tex-table function
particles.sort(key=lambda k: (k.psq, k.mom1, k.mom2, k.energy, k.flav1, k.flav2))

for ensem in ("32", "24"):
    for psq in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]:
        for samp in [("Bootstrap","boot"), ("Jackknife","jack")]:
            textable_super(particles, psq, ensem, samp[0], "/latticeQCD/raid6/ruairi/freeparticle_energies/notes/tables/twoparticles" + ensem + "_P" + psq + "_" + samp[1])
