import xml.etree.cElementTree as ET
import os
import sys

# Initialise SigMond, most of this can be taken from filenames?
def initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type):
    # Get filenames, filenumbers, etc
    # TODO: use map/dict to associate filemax with given corr_path -- current while loops look shite
    i = 0
    filemax = []
    if(obs_type == "BLCorr"):
        while i < len(corr_paths):
            filenums = list()
            name = ""
            for corr_paths[i],dirnames,filenames in os.walk(corr_paths[i]):
                for file in filenames:
                    fileExt = os.path.splitext(file)[-1]
                    filenums.append(int(fileExt[1:]))
                    name = os.path.splitext(file)[-2]

            filemax.append(max(filenums))

            corr_paths[i] += name
            i += 1
        
    # Start the XML here:
    ET.SubElement(init, "ProjectName").text = proj_name
    ET.SubElement(init, "LogFile").text = logfile
    ET.SubElement(init, "EchoXML")

    # MCBinsInfo -- Change to take EnsembleInfo from filenames or as argument?
    mcbins = ET.SubElement(init, "MCBinsInfo")
    if(ensemble == "32_860"):
        ET.SubElement(mcbins, "MCEnsembleInfo").text = "clover_s32_t256_ud860_s743"
    elif(ensemble == "24_860"):
        ET.SubElement(mcbins, "MCEnsembleInfo").text = "clover_s24_t128_ud860_s743"
    elif(ensemble == "24_840"):
        ET.SubElement(mcbins, "MCEnsembleInfo").text = "clover_s24_t128_ud840_s743"
    elif(ensemble == "16_840"):
        ET.SubElement(mcbins, "MCEnsembleInfo").text = "clover_s16_t128_ud840_s743"
    elif(ensemble == "phi_rho"):
        ET.SubElement(mcbins, "MCEnsembleInfo").text = "phirho_s32_t48_mp0150_mr0350_lm0050_0300|9695|1|32|32|32|48"
    else:
        print("You fucked up the ensemble info, fix it.")
        sys.exit()

    # MCSamplingInfo
    mcsample = ET.SubElement(init, "MCSamplingInfo")
    if(sampling == "Jackknife"):
        ET.SubElement(mcsample, "Jackknife")
    elif(sampling == "Bootstrap"):
        boots = ET.SubElement(mcsample, "Bootstrapper")
        ET.SubElement(boots, "NumberResamplings").text = "2048"
        ET.SubElement(boots, "Seed").text = "6754"
        ET.SubElement(boots, "BootSkip").text = "127"
        ET.SubElement(boots, "Precompute")
    else:
        print("Something's wrong with the init parameters, fix it.")
        sys.exit()

    # MCObservables
    mcobs = ET.SubElement(init, "MCObservables")
    if(obs_type == "BLCorr"):
        BLcorrs = ET.SubElement(mcobs, "BLCorrelatorData")
        i = 0
        while i < len(corr_paths):
            files = ET.SubElement(BLcorrs, "FileListInfo")
            ET.SubElement(files, "FileNameStub").text = corr_paths[i]
            ET.SubElement(files, "MinFileNumber").text = "0"
            ET.SubElement(files, "MaxFileNumber").text = str(filemax[i])
            # ET.SubElement(files, "FileMode").text = "Overwrite"
            i +=1
    elif(obs_type == "bins"):
        bins = ET.SubElement(mcobs, "BinData")
        for x in corr_paths:
            ET.SubElement(bins, "FileName").text = str(x)
    elif(obs_type == "samplings"):
        bins = ET.SubElement(mcobs, "SamplingData")
        for x in corr_paths:
            ET.SubElement(bins, "FileName").text = str(x)        
    else:
        print("Wrong MCObs type, fit it.")
        sys.exit()
