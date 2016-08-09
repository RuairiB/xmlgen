import xml.etree.cElementTree as ET
import os

def initialize(corr_path, oplist_file, proj_name, logfile, init):
    # Get filenames, filenumbers, etc
    filenums = list()
    name = ""
    for corr_path,dirnames,filenames in os.walk(corr_path):
        for file in filenames:
            fileExt = os.path.splitext(file)[-1]
            filenums.append(int(fileExt[1:]))
            name = os.path.splitext(file)[-2]
            
    filemax = max(filenums)

    corr_path += name

    # Start the XML here:
    ET.SubElement(init, "ProjectName").text = proj_name
    ET.SubElement(init, "LogFile").text = logfile
    ET.SubElement(init, "EchoXML")
    
    # MCObservables
    mcobs = ET.SubElement(init, "MCObservables")
    ET.SubElement(mcobs, "MCEnsembleInfo").text = "clover_s32_t256_ud860_s743"
    corrdat = ET.SubElement(mcobs, "CorrelatorData")
    files = ET.SubElement(corrdat, "FileListInfo")
    ET.SubElement(files, "FileNameStub").text = corr_path
    ET.SubElement(files, "MinFileNumber").text = "0"
    ET.SubElement(files, "MaxFileNumber").text = str(filemax)
    
    specs = ET.SubElement(mcobs, "Specifications")
    herm_corr = ET.SubElement(specs, "HermitianCorrelationMatrix")
    corr_matrix = ET.SubElement(herm_corr, "AssignName").text = proj_name
    oplist = open(oplist_file).read().splitlines()
    for f in oplist:
        ET.SubElement(herm_corr, "OperatorString").text = f
        
    boots = ET.SubElement(init, "Bootstrapper")
    ET.SubElement(boots, "NumberResamplings").text = "1024"
    ET.SubElement(boots, "Seed").text = "6754"
    ET.SubElement(boots, "BootSkip").text = "127"
    ET.SubElement(boots, "Precompute")


# Indent for easy reading
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
