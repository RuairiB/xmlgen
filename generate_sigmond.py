#import xml.etree.cElementTree as ET
import lxml.etree as ET
import os
# from init import *

corr_path = "/latticeQCD/raid8/laph/clover_s32_t256_ud860_s743/bosonic_correlators/isodoublet_strange/mom_0_0_0/T1u_1/" #corr_32_860_B_2I1_S1_P0_T1u"

filenums=list()
for corr_path,dirnames,filenames in os.walk(corr_path):
    for file in filenames:
        fileExt=os.path.splitext(file)[-1]
        filenums.append(fileExt)

print filenums
        
filemax = 1 # max(filenums)


root = ET.Element("SigMonD")

init = ET.SubElement(root, "Initialize")
tasks = ET.SubElement(root, "TaskSequence")


ET.SubElement(init, "ProjectName").text = "some project name"
ET.SubElement(init, "LogFile").text = "some logfile.xml"
ET.SubElement(init, "EchoXML")

mcobs = ET.SubElement(init, "MCObservables")
ET.SubElement(mcobs, "MCEnsembleInfo").text = "clover_s32_t256_ud860_s743"
corrdat = ET.SubElement(mcobs, "CorrelatorData")
files = ET.SubElement(corrdat, "FileListInfo")
# ET.SubElement(files, "FileNameStub").text = corr_path
ET.SubElement(files, "MinFileNumber").text = "0"
ET.SubElement(files, "MaxFileNumber").text = str(filemax)

tree = ET.ElementTree(root)
tree.write("filename.xml", pretty_print=True)
