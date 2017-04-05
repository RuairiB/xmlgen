import xml.etree.cElementTree as ET
import os
import sys
from utils import *

# SigMond tasks
# TO DO:
# DoCorrMatrixZMagSquares
# DoRotCorrMatReorderLevelsByEnergy
# Flesh out reading/writing bins/samplings, etc
# C(t+1) - C(t)
# Fit to two correlators?

# Go through header files for single pivot and rolling pivot, this could do with some more fleshing out
def rotatematrix(tasks, piv_type, oplist, herm, vev, rotop, piv_name, tmin, tmax, tnorm, tmet, tdiag, piv_file, rotcorr_file, plot_sampling, effenergytype, plotstub):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoCorrMatrixRotation"
    ET.SubElement(task, "MinTimeSep").text = str(tmin)
    ET.SubElement(task, "MaxTimeSep").text = str(tmax)
    if piv_type == "SinglePivot":
        ET.SubElement(task, "Type").text = "SinglePivot"
        pivoter = ET.SubElement(task, "SinglePivotInitiate")
    elif piv_type == "RollingPivot":
        ET.SubElement(task, "Type").text = "RollingPivot"
        pivoter = ET.SubElement(task, "RollingPivotInitiate")
    else:
        print("need to implement other pivot types, check if in SigMonD first")
        sys.exit()

    matrixinfo = ET.SubElement(pivoter, "CorrelatorMatrixInfo")
    for x in oplist:
        if any(isospin in x for isospin in ["isosinglet", "isodoublet", "isotriplet", "isoquartet"]):
            ET.SubElement(matrixinfo, "GIOperatorString").text = x
        else:
            ET.SubElement(matrixinfo, "BLOperatorString").text = x
            
    if herm:
        ET.SubElement(matrixinfo, "HermitianMatrix")
    if vev:
        ET.SubElement(matrixinfo, "SubtractVEV")

    rotatedop = ET.SubElement(pivoter, "RotatedCorrelator")
    ET.SubElement(rotatedop, "GIOperatorString").text = rotop

    ET.SubElement(pivoter, "AssignName").text = piv_name
    ET.SubElement(pivoter, "NormTime").text = str(tnorm)
    ET.SubElement(pivoter, "MetricTime").text = str(tmet)
    ET.SubElement(pivoter, "DiagonalizeTime").text = str(tdiag)
    ET.SubElement(pivoter, "MinimumInverseConditionNumber").text = "0.01"
    ET.SubElement(pivoter, "NegativeEigenvalueAlarm").text = "-0.01"
    ET.SubElement(pivoter, "CheckMetricErrors")
    ET.SubElement(pivoter, "CheckCommonMetrixMatrixNullSpace")

    writepiv = ET.SubElement(pivoter, "WritePivotToFile")
    ET.SubElement(writepiv, "PivotFileName").text = piv_file
    ET.SubElement(writepiv, "Overwrite")

    writecorr = ET.SubElement(task, "WriteRotatedCorrToFile")
    ET.SubElement(writecorr, "RotatedCorrFileName").text = rotcorr_file
    ET.SubElement(writecorr, "Type").text = "bins" # Or samplings for single pivot?
    ET.SubElement(writecorr, "Overwrite")

    plots = ET.SubElement(task, "PlotRotatedEffectiveEnergies")
    ET.SubElement(plots, "SamplingMode").text = plot_sampling
    if any(effenergytype == x for x in ["TimeForward", "TimeForwardPlusConst", "TimeSymmetric", "TimeSymmetricPlusConst"]):
        ET.SubElement(plots, "EffEnergyType").text = effenergytype
    else:
        print("give a better eff energy type")
        sys.exit()

    ET.SubElement(plots, "TimeStep").text = "3"
    ET.SubElement(plots, "PlotFileStub").text = plotstub
    ET.SubElement(plots, "SymbolColor").text = "blue"
    ET.SubElement(plots, "SymbolType").text = "circle"
    ET.SubElement(plots, "MaxErrorToPlot").text = "1.0"


# def zfactors(tasks, piv_type, ):
#     task = ET.SubElement(tasks, "Task")

#     ET.SubElement(task, "Action").text = "DoCorrMatrixZMagSquares"
#     if piv_type == "SinglePivot":
#         ET.SubElement(task, "Type").text = "SinglePivot"
#         pivoter = ET.SubElement(task, "SinglePivotInitiate")
#     elif piv_type == "RollingPivot":
#         ET.SubElement(task, "Type").text = "RollingPivot"
#         pivoter = ET.SubElement(task, "RollingPivotInitiate")
#     else:
#         print("need to implement other pivot types, check if in SigMonD first")
#         sys.exit()

    



# Effective mass fit to correlator data
def dofit(tasks, operator, fitname, tmin, tmax, fitfn, minimizer, plotfile, psq, energies, refenergy, sampling="Bootstrap"):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoFit"
    ET.SubElement(task, "Type").text = "TemporalCorrelator"

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

    ET.SubElement(task, "SamplingMode").text = sampling

    fit = ET.SubElement(task, "TemporalCorrelatorFit")

    # remove need for optype variable, check operator string for flav vs isospin to determine type
    flav = ["pion", "kaon", "eta", "phi", "kbar", "nucleon", "delta", "omega", "sigma", "lambda", "xi"]
    isospin = ["singlet", "doublet", "triplet", "quartet"]

    if any(i in operator for i in flav):
        op = ET.SubElement(fit, "BLOperatorString").text = operator
    elif any(i in operator for i in isospin):
        op = ET.SubElement(fit, "GIOperatorString").text = operator
    else:
        print("Help please, I need an operator type I understand.")
        sys.exit()

    ET.SubElement(fit, "MinimumTimeSeparation").text = str(tmin)
    ET.SubElement(fit, "MaximumTimeSeparation").text = str(tmax)
    ET.SubElement(fit, "LargeTimeNoiseCutoff").text = "1.0"

    model = ET.SubElement(fit, "Model")
    ET.SubElement(model, "Type").text = fitfn

    if(fitfn == "TimeSymSingleExponential"):
        fitmodel = "tsse"
    elif(fitfn == "TimeSymSingleExponentialPlusConstant"):
        fitmodel = "tsseC"
    elif(fitfn == "TimeSymTwoExponential"):
        fitmodel = "tste"
    elif(fitfn == "TimeSymTwoExponentialPlusConstant"):
        fitmodel = "tsteC"
    elif(fitfn == "TimeSymGeomSeriesExponential"):
        fitmodel = "tsgs"
    else:
        print("model confusion, fix me")
        sys.exit()

    if(len(fitname) < 8):
        obsname = str(fitname) + "_" + str(tmin) + "_" + str(tmax) + "P" + str(psq) + fitmodel
    else:
        print("fitname: " + fitname + " may be too long for obsnames")
        sys.exit()
    # if(fitfn == "TimeSymSingleExponential" or fitfn == "TimeSymSingleExponentialPlusConstant"):
    #     energies.append("En_" + obsname)
    # else:
    #     energies.append("En1_" + obsname)
    energies.append("E1_" + obsname)

    eng = ET.SubElement(model, "Energy")
    ET.SubElement(eng, "Name").text = "E1_" + obsname
    ET.SubElement(eng, "IDIndex").text = "0"
    amp = ET.SubElement(model, "Amplitude")
    ET.SubElement(amp, "Name").text = "A1_" + obsname
    ET.SubElement(amp, "IDIndex").text = "0"
    eng1 = ET.SubElement(model, "FirstEnergy")
    ET.SubElement(eng1, "Name").text = "E1_" + obsname
    ET.SubElement(eng1, "IDIndex").text = "0"
    amp1 = ET.SubElement(model, "FirstAmplitude")
    ET.SubElement(amp1, "Name").text = "A1_" + obsname
    ET.SubElement(amp1, "IDIndex").text = "0"
    eng2 = ET.SubElement(model, "SqrtGapToSecondEnergy")
    ET.SubElement(eng2, "Name").text = "E2_" + obsname
    ET.SubElement(eng2, "IDIndex").text = "0"
    amp2 = ET.SubElement(model, "SecondAmplitudeRatio")
    ET.SubElement(amp2, "Name").text = "A2_" + obsname
    ET.SubElement(amp2, "IDIndex").text = "0"
    const = ET.SubElement(model, "AddedConstant")
    ET.SubElement(const, "Name").text = "C_" + obsname
    ET.SubElement(const, "IDIndex").text = "0"

    plot = ET.SubElement(fit, "DoEffectiveEnergyPlot")
    ET.SubElement(plot, "PlotFile").text = plotfile
    ET.SubElement(plot, "CorrName").text = "standard"
    ET.SubElement(plot, "TimeStep").text = "3"
    ET.SubElement(plot, "SymbolColor").text = "blue"
    ET.SubElement(plot, "SymbolType").text = "circle"
    ET.SubElement(plot, "Goodness").text = "chisq"
    if (refenergy != "none"):
        ref = ET.SubElement(plot, "ReferenceEnergy")
        ET.SubElement(ref, "Name").text = refenergy
        ET.SubElement(ref, "IDIndex").text = "0"
    ET.SubElement(plot, "ShowApproach")


def writesamplings(tasks, energies, energyfile, sampling="Bootstrap"):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "WriteSamplingsToFile"
    ET.SubElement(task, "SamplingMode").text = sampling
    ET.SubElement(task, "FileName").text = energyfile
    ET.SubElement(task, "FileMode").text = "overwrite"

    for x in energies:
        obs = ET.SubElement(task, "MCObservable")
        ET.SubElement(obs, "ObsName").text = x
        ET.SubElement(obs, "Index").text = "0"


def readsamplings(tasks, filename, sampling, mcobs):
    task = ET.SubElement(tasks, "Task")
    ET.SubElement(task, "Action").text = "ReadSamplingsFromFile"
    ET.SubElement(task, "SamplingMode").text = sampling
    ET.SubElement(task, "FileName").text = filename
    for x in mcobs:
        obs = ET.SubElement(task, "MCObservable")
        ET.SubElement(obs, "ObsName").text = str(x)
        ET.SubElement(obs, "IDIndex").text = "0"

        
def diagonalenergyplots(tasks, oplist, filestub, sampling="Jackknife"):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoPlot"
    ET.SubElement(task, "Type").text = "EffectiveEnergies"
    ET.SubElement(task, "EffEnergyType").text = "TimeForward" # flag for forward vs symmetric?
    ET.SubElement(task, "TimeStep").text = "3"

    corrset = ET.SubElement(task, "DiagonalCorrelatorSet")
    seq = ET.SubElement(corrset, "Sequential")
    for x in oplist:
        ET.SubElement(seq, "BLOperatorString").text = x

    ET.SubElement(task, "Sampling").text = sampling
    ET.SubElement(task, "PlotFileStub").text = filestub
    ET.SubElement(task, "CorrName").text = "standard"


def momaverage(tasks, opfile, psq, binfile, tmin, tmax, hermitian):
    task = ET.SubElement(tasks, "Task")
    operators = getopsdef(opfile, psq)
    if not operators:
        print("uuh operator list is empty for PSQ = " + str(psq) + ". try again.")
        sys.exit()

    # Make available constituent momenta
    if(psq == 0):
        mom = ["0,0,0"]
    if(psq == 1):
        mom = ["0,0,1", "0,0,-1", "0,1,0", "0,-1,0", "1,0,0", "-1,0,0"]
    if(psq == 2):
        mom = ["0,1,1", "0,-1,1", "0,1,-1", "0,-1,-1", "1,0,1", "1,0,-1", "-1,0,1", "-1,0,-1", "1,1,0", "1,-1,0", "-1,1,0", "-1,-1,0"]
    if(psq == 3):
        mom = ["1,1,1", "1,1,-1", "1,-1,1", "-1,1,1", "-1,-1,1", "-1,1,-1", "1,-1,-1", "-1,-1,-1"]
    if(psq == 4):
        mom = ["0,0,2", "0,0,-2", "0,2,0", "0,-2,0", "2,0,0", "-2,0,0"]
    if(psq == 5):
        mom = ["1,2,0", "-1,0,-2", "-1,0,2", "-1,2,0", "-2,-1,0", "-2,0,-1", "-2,0,1", "-2,1,0", "0,-1,-2", "0,-1,2", "0,-2,-1", "0,-2,1", "2,1,0", "2,0,1", "2,0,-1", "2,-1,0", "-1,-2,0", "1,0,2", "1,0,-2", "1,-2,0", "0,2,1", "0,1,2", "0,2,-1", "0,1,-2"]
    if(psq == 6):
        mom = ["1,1,2", "-1,-2,-1", "-1,-2,1", "-1,1,-2", "-1,1,2", "-1,-1,-2", "-1,2,-1", "-1,2,1", "-2,-1,-1", "-2,-1,1", "-2,1,-1", "-2,1,1", "1,-1,-2", "1,-1,2", "1,-2,-1", "1,-2,1", "1,1,-2", "-1,-1,2", "1,2,-1", "1,2,1", "2,-1,-1", "2,-1,1", "2,1,-1", "2,1,1"]

    # Get flavour info -- assumes all the same for now
    templist = []
    for x in operators:
        if("pion" in x):
            isospin = "isotriplet"
            flav = "pion"
            templist.append(x)
        elif("kaon" in x):
            isospin = "isodoublet"
            flav = "kaon"
            templist.append(x)
        elif("eta" in x):
            isospin = "isosinglet"
            flav = "eta"
            templist.append(x)
        elif("nucleon" in x):
            isospin = "isodoublet"
            flav = "nucleon"
            templist.append(x)

    # Strip all but displacement info
    for i,s in enumerate(templist):
        templist[i] = s.split(") ", 1)[-1]
    # Remove duplicates
    oplist = []
    for i in templist:
        if i not in oplist:
            oplist.append(i)


    ET.SubElement(task, "Action").text = "DoObsFunction"
    ET.SubElement(task, "Type").text = "CorrelatorMatrixSuperposition"
    results = ET.SubElement(task, "ResultOperatorOrderedList")
    # GIOperatorStrings for resultant averaged matrix here
    for opname in oplist:
        ET.SubElement(results, "GIOperatorString").text = isospin + " " + "P=(" + mom[0] + ") " + opname

    # BL (or GI??) OperatorStrings to be averaged here
    # loop over list of matrices to be averaged for given psq
    for x in mom:
        matrix = ET.SubElement(task, "OperatorOrderedList")
        for opname in oplist:
            item = ET.SubElement(matrix, "Item")
            ET.SubElement(item, "BLOperatorString").text = flav + " " + "P=(" + x + ") " + opname
            ET.SubElement(item, "Coefficient").text = "1.0"

    ET.SubElement(task, "MinimumTimeSeparation").text = str(tmin)
    ET.SubElement(task, "MaximumTimeSeparation").text = str(tmax)
    if(hermitian):
        ET.SubElement(task, "HermitianMatrix")
    ET.SubElement(task, "WriteToBinFile").text = binfile
    ET.SubElement(task, "FileMode").text = "overwrite"
    
    
def operatoraverage(tasks, ops, opresult, binfile, tmin, tmax, hermitian):
    task = ET.SubElement(tasks, "Task")
    if not ops:
        print("uuh operator list is empty. try again.")
        sys.exit()

    flav = ["pion", "kaon", "eta", "phi", "kbar", "nucleon", "delta", "omega", "sigma", "lambda", "xi"]
    isospin = ["singlet", "doublet", "triplet", "quartet"]
        
    # associate GI or BL with each operator? -- check for isospin of flavour
    oplist = []
    for x in ops:
        if (any(i in x for i in flav)):
            oplist.append((x, "BL"))
        elif (any(i in x for i in isospin)):
            oplist.append((x, "GI"))
        else:
            print("can't determine optype for " + x)
            sys.exit()

    ET.SubElement(task, "Type").text = "CorrelatorMatrixSuperposition"
    results = ET.SubElement(task, "ResultOperatorOrderedList")
    ET.SubElement(results, "GIOperatorString").text = opresult

    for x in oplist:
        matrix = ET.SubElement(task, "OperatorOrderedList")
        item = ET.SubElement(matrix, "Item")
        ET.SubElement(item, x[1] + "OperatorString").text = str(x[0])
        ET.SubElement(item, "Coefficient").text = "1.0"

    ET.SubElement(task, "MinimumTimeSeparation").text = str(tmin)
    ET.SubElement(task, "MaximumTimeSeparation").text = str(tmax)
    if(hermitian):
        ET.SubElement(task, "HermitianMatrix")
    ET.SubElement(task, "WriteToBinFile").text = binfile
    ET.SubElement(task, "FileMode").text = "overwrite"


def aspect_ratio(tasks, Ns, ordered_energies, xi_name, plotfile, minimizer, sampling):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoFit"
    ET.SubElement(task, "Type").text = "AnisotropyFromDispersion"

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

    ET.SubElement(task, "SamplingMode").text = sampling
    ET.SubElement(task, "CovMatCalcSamplingMode").text = sampling
    
    fit = ET.SubElement(task, "AnisotropyFromDispersionFit")
    ET.SubElement(fit, "SpatialExtentNumSites").text = str(Ns)
    i = 0
    for x in ordered_energies:
        energy = ET.SubElement(fit, "Energy")
        ET.SubElement(energy, "Name").text = x
        ET.SubElement(energy, "IDIndex").text = "0"
        ET.SubElement(energy, "IntMomSquared").text = str(i)
        i += 1

    anis = ET.SubElement(fit, "Anisotropy")
    ET.SubElement(anis, "Name").text = "xi" + xi_name
    ET.SubElement(anis, "IDIndex").text = "0"
    
    msq = ET.SubElement(fit, "RestMass")
    ET.SubElement(msq, "Name").text = "msq" + xi_name
    ET.SubElement(msq, "IDIndex").text = "0"

    plot = ET.SubElement(fit, "DoPlot")
    ET.SubElement(plot, "PlotFile").text = plotfile
    ET.SubElement(plot, "CorrName").text = "standard"
    ET.SubElement(plot, "TimeStep").text = "3"
    ET.SubElement(plot, "SymbolColor").text = "blue"
    ET.SubElement(plot, "SymbolType").text = "circle"
    ET.SubElement(plot, "Goodness").text = "chisq"


def add_obs(tasks, obs_strs, result_str, mode):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoObsFunction"
    ET.SubElement(task, "Type").text = "LinearSuperposition"

    result = ET.SubElement(task, "Result")
    ET.SubElement(result, "Name").text = result_str
    ET.SubElement(result, "IDIndex").text = "0"

    # # Ensure obs_strs a list of tuples with ObsName and coefficient
    # for i in obs_strs:
    #     if(type(i) != tuple):
    #         print("gis some tuples please")
    #         sys.exit()
    #     elif(len(i) != 2):
    #         print("wrong tuple length")
    #         sys.exit()

    for x in obs_strs:
        summand = ET.SubElement(task, "Summand")
        obs = ET.SubElement(summand, "MCObservable")
        ET.SubElement(obs, "ObsName").text = x
        ET.SubElement(obs, "Index").text = "0"
        ET.SubElement(summand, "Coefficient").text = "1.0"

    # Sampling mode or "bins"
    ET.SubElement(task, "Mode").text = mode

    
def ref_ratio(tasks, obs_str, ref_str, result_str, mode):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoObsFunction"
    ET.SubElement(task, "Type").text = "Ratio"

    result = ET.SubElement(task, "Result")
    ET.SubElement(result, "Name").text = result_str
    ET.SubElement(result, "IDIndex").text = "0"

    numerator = ET.SubElement(task, "Numerator")
    obs = ET.SubElement(numerator, "MCObservable")
    ET.SubElement(obs, "ObsName").text = obs_str
    ET.SubElement(obs, "Index").text = "0"

    denominator = ET.SubElement(task, "Denominator")
    obs = ET.SubElement(denominator, "MCObservable")
    ET.SubElement(obs, "ObsName").text = ref_str
    ET.SubElement(obs, "Index").text = "0"

    # Sampling mode or "bins"
    ET.SubElement(task, "Mode").text = mode
