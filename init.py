import xml.etree.cElementTree as ET
import os
import sys

# Initialise SigMond, most of this can be taken from filenames?
def initialize(init, corr_paths, proj_name, logfile, sampling, ensemble, obs_type, echo=False):
    # Get filenames, filenumbers, etc
    # TODO: use map/dict to associate filemax with given corr_path -- current loops look shite
    if isinstance(obs_type, basestring):
        temp = obs_type
        obs_type = []
        for x in corr_paths:
            obs_type.append(temp)

    if len(obs_type) != len(corr_paths):
        print("some list length problems")
        sys.exit()

    i = 0
    filemax = []
    while i < len(corr_paths):
        if(obs_type[i] == "BLCorr"):
            filenums = list()
            name = ""
            for corr_paths[i],dirnames,filenames in os.walk(corr_paths[i]):
                for file in filenames:
                    fileExt = os.path.splitext(file)[-1]
                    filenums.append(int(fileExt[1:]))
                    name = os.path.splitext(file)[-2]

            filemax.append(max(filenums))

            corr_paths[i] += name
        else:
            filemax.append(0)
        i += 1

    # Start the XML here:
    ET.SubElement(init, "ProjectName").text = proj_name
    ET.SubElement(init, "LogFile").text = logfile
    if echo:
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
    elif(ensemble == "phi_rho32"):
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
    i = 0
    if any(x == "BLCorr" for x in obs_type):
        BLcorrs = ET.SubElement(mcobs, "BLCorrelatorData")
    if any(x == "bins" for x in obs_type):
        bins = ET.SubElement(mcobs, "BinData")
    if any(x == "samplings" for x in obs_type):
        samps = ET.SubElement(mcobs, "SamplingData")

    while i < len(corr_paths):
        if(obs_type[i] == "BLCorr"):
            files = ET.SubElement(BLcorrs, "FileListInfo")
            ET.SubElement(files, "FileNameStub").text = corr_paths[i]
            ET.SubElement(files, "MinFileNumber").text = "0"
            ET.SubElement(files, "MaxFileNumber").text = str(filemax[i])
        elif(obs_type[i] == "bins"):
            ET.SubElement(bins, "FileName").text = corr_paths[i]
        elif(obs_type[i] == "samplings"):
            ET.SubElement(samps, "FileName").text = corr_paths[i]
        else:
            print("Wrong MCObs type, fit it.")
            sys.exit()
        i += 1
