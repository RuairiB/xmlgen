import xml.etree.cElementTree as ET
import os

# Old SigMond rotation input, routines need to be run separately for some unknown reason...
def oldrotateA(mintime, maxtime, proj_name, file_tail, norm_time, metric_time, diag_time, cond_num, tasks):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoCorrMatrixRotation"
    ET.SubElement(task, "MinTimeSep").text = str(mintime)
    ET.SubElement(task, "MaxTimeSep").text = str(maxtime)
    ET.SubElement(task, "Type").text = "SinglePivot"

    piv = ET.SubElement(task, "SinglePivotInitiate")
    ET.SubElement(piv, "RotationName").text = proj_name
    ET.SubElement(piv, "AssignName").text = "Piv" + proj_name

    corr = ET.SubElement(piv, "CorrelatorMatrixInfo")
    ET.SubElement(corr, "Name").text = proj_name

    ET.SubElement(piv, "NormTime").text = str(norm_time)
    ET.SubElement(piv, "MetricTime").text = str(metric_time)
    ET.SubElement(piv, "DiagonalizeTime").text = str(diag_time)
    ET.SubElement(piv, "MinimumInverseConditionNumber").text = cond_num

    fileout = ET.SubElement(piv, "WriteToFile")
    ET.SubElement(fileout, "Filename").text = "SinglePivot_" + file_tail
    ET.SubElement(fileout, "Overwrite")


def oldrotateB(mintime, maxtime, proj_name, file_tail, tasks):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoCorrMatrixRotation"
    ET.SubElement(task, "MinTimeSep").text = str(mintime)
    ET.SubElement(task, "MaxTimeSep").text = str(maxtime)
    ET.SubElement(task, "Type").text = "SinglePivot"

    piv = ET.SubElement(task, "SinglePivotInitiate")
    piv_file = ET.SubElement(piv, "ReadFromFile")
    ET.SubElement(piv_file, "Name").text = "SinglePivot_" + file_tail
    ET.SubElement(piv, "AssignName").text = "Piv" + proj_name
    
    fileout = ET.SubElement(task, "WriteToFile")
    ET.SubElement(fileout, "Filename").text = "RotatedCorrelators_" + file_tail
    ET.SubElement(fileout, "Overwrite")


    
