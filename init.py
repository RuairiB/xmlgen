import xml.etree.cElementTree as ET

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
ET.Subelement(files, FileNameStub).text = correlator_path


# tree = ET.ElementTree(root)
# tree.write("filename.xml")
