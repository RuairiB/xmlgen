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

def readpivot(task, piv_type, piv_file, piv_name):
    if piv_type == "SinglePivot":
        ET.SubElement(task, "Type").text = "SinglePivot"
        pivoter = ET.SubElement(task, "SinglePivotInitiate")
    elif piv_type == "RollingPivot":
        ET.SubElement(task, "Type").text = "RollingPivot"
        pivoter = ET.SubElement(task, "RollingPivotInitiate")
    else:
        print("need to implement other pivot types, check if in SigMonD first")
        sys.exit()
    
    read = ET.SubElement(pivoter, "ReadPivotFromFile")
    ET.SubElement(read, "PivotFileName").text = piv_file
    ET.SubElement(pivoter, "AssignName").text = piv_name


def getoptype(operator):
    flav = ["pion", "kaon", "eta", "phi", "kbar", "nucleon", "delta", "omega", "sigma", "lambda", "xi"]
    isospin = ["singlet", "doublet", "triplet", "quartet"]

    if any(i in operator for i in flav):
        return "BLOperatorString"
    elif any(i in operator for i in isospin):
        return "GIOperatorString"
    else:
        print("Help please, I need an operator type I understand.")
        sys.exit()


def modelparams(elem, obsname):
    eng = ET.SubElement(elem, "Energy")
    ET.SubElement(eng, "Name").text = "E1_" + obsname
    ET.SubElement(eng, "IDIndex").text = "0"
    amp = ET.SubElement(elem, "Amplitude")
    ET.SubElement(amp, "Name").text = "A1_" + obsname
    ET.SubElement(amp, "IDIndex").text = "0"
    eng1 = ET.SubElement(elem, "FirstEnergy")
    ET.SubElement(eng1, "Name").text = "E1_" + obsname
    ET.SubElement(eng1, "IDIndex").text = "0"
    amp1 = ET.SubElement(elem, "FirstAmplitude")
    ET.SubElement(amp1, "Name").text = "A1_" + obsname
    ET.SubElement(amp1, "IDIndex").text = "0"
    eng2 = ET.SubElement(elem, "SqrtGapToSecondEnergy")
    ET.SubElement(eng2, "Name").text = "E2_" + obsname
    ET.SubElement(eng2, "IDIndex").text = "0"
    amp2 = ET.SubElement(elem, "SecondAmplitudeRatio")
    ET.SubElement(amp2, "Name").text = "A2_" + obsname
    ET.SubElement(amp2, "IDIndex").text = "0"
    const = ET.SubElement(elem, "AddedConstant")
    ET.SubElement(const, "Name").text = "C_" + obsname
    ET.SubElement(const, "IDIndex").text = "0"


def minimizerinfo(task, minimizer):
    mini = ET.SubElement(task, "MinimizerInfo")
    if minimizer == "Minuit2":
        ET.SubElement(mini, "Method").text = "Minuit2"
    elif minimizer == "Minuit2NoGradient":
        ET.SubElement(mini, "Method").text = "Minuit2NoGradient"
    elif minimizer == "LMDer":
        ET.SubElement(mini, "Method").text = "LMDer"
    elif minimizer == "NL2Sol":
        ET.SubElement(mini, "Method").text = "NL2Sol"
    else:
        print("give me some minimizer info\n")
        sys.exit()

    ET.SubElement(mini, "ParameterRelTol").text = "1e-6"
    ET.SubElement(mini, "ChiSquareRelTol").text = "1e-4"
    ET.SubElement(mini, "MaximumIterations").text = "2048"
    ET.SubElement(mini, "Verbosity").text = "Low"


