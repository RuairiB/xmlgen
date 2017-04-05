## Various functions and classes for using XMLgen with SigMond
import xml.etree.cElementTree as ET
import os
import sys

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

# Get list of operators with given P^2 from opdefs file
def getopsdef(filename, psq):
    opdefs = file(filename)
    operators = []
    psq0 = ["0,0,0"]
    psq1 = ["0,0,1", "0,0,-1", "0,1,0", "0,-1,0", "1,0,0", "-1,0,0"]
    psq2 = ["0,1,1", "0,-1,1", "0,1,-1", "0,-1,-1", "1,0,1", "1,0,-1", "-1,0,1", "-1,0,-1", "1,1,0", "1,-1,0", "-1,1,0", "-1,-1,0"]
    psq3 = ["1,1,1", "1,1,-1", "1,-1,1", "-1,1,1", "-1,-1,1", "-1,1,-1", "1,-1,-1", "-1,-1,-1"]
    psq4 = ["0,0,2", "0,0,-2", "0,2,0", "0,-2,0", "2,0,0", "-2,0,0"]
    psq5 = ["-1,-2,0", "-1,0,-2", "-1,0,2", "-1,2,0", "-2,-1,0", "-2,0,-1", "-2,0,1", "-2,1,0", "0,-1,-2", "0,-1,2", "0,-2,-1", "0,-2,1", "2,1,0", "2,0,1", "2,0,-1", "2,-1,0", "1,2,0", "1,0,2", "1,0,-2", "1,-2,0", "0,2,1", "0,1,2", "0,2,-1", "0,1,-2"]
    psq6 = ["-1,-1,2", "-1,-2,-1", "-1,-2,1", "-1,1,-2", "-1,1,2", "-1,-1,-2", "-1,2,-1", "-1,2,1", "-2,-1,-1", "-2,-1,1", "-2,1,-1", "-2,1,1", "1,-1,-2", "1,-1,2", "1,-2,-1", "1,-2,1", "1,1,-2", "1,1,2", "1,2,-1", "1,2,1", "2,-1,-1", "2,-1,1", "2,1,-1", "2,1,1"]

    if psq == 0:
        for line in opdefs:
            if any(x in line for x in psq0):
                operators.append(line)
    if psq == 1:
        for line in opdefs:
            if any(x in line for x in psq1):
                operators.append(line)
    if psq == 2:
        for line in opdefs:
            if any(x in line for x in psq2):
                operators.append(line)
    if psq == 3:
        for line in opdefs:
            if any(x in line for x in psq3):
                operators.append(line)
    if psq == 4:
        for line in opdefs:
            if any(x in line for x in psq4):
                operators.append(line)
    if psq == 5:
        for line in opdefs:
            if any(x in line for x in psq5):
                operators.append(line)
    if psq == 6:
        for line in opdefs:
            if any(x in line for x in psq6):
                operators.append(line)

    for i, s in enumerate(operators):
        operators[i] = s.replace(']', '')
    for i, s in enumerate(operators):
        operators[i] = s.replace('\",', '')
    for i, s in enumerate(operators):
        operators[i] = s.replace('\"', '')
    for i, s in enumerate(operators):
        operators[i] = s.strip()

    return operators


def str_name(blah):
    return [ k for k,v in locals().iteritems() if v is blah][0]

def shortform(fitfn):
    if fitfn == "TimeSymSingleExponential":
        return "tsse"
    elif fitfn == "TimeSymSingleExponentialPlusConstant":
        return "tsseC"
    elif fitfn == "TimeSymTwoExponential":
        return "tste"
    elif fitfn == "TimeSymTwoExponentialPlusConstant":
        return "tsteC"
    elif fitfn == "TimeSymGeomSeriesExponential":
        return "tsgs"
    elif fitfn == "TimeForwardSingleExponential":
        return "tfse"
    elif fitfn == "TimeForwardSingleExponentialPlusConstant":
        return "tfseC"
    elif fitfn == "TimeForwardTwoExponential":
        return "tfte"
    elif fitfn == "TimeForwardTwoExponentialPlusConstant":
        return "tfteC"
    elif fitfn == "TimeForwardGeomSeriesExponential":
        return "tfgs"
    else:
        print("I need a valid fit function dickhead.")
        sys.exit()
