import xml.etree.cElementTree as ET
import os
import sys
from utils import *

# SigMond tasks
# TO DO:
# Update TO DO list...
# Entire rotation/reordering/z factor process -- Improve functionality

# Go through header files for single pivot and rolling pivot, this could do with some more fleshing out
def rotatematrix(tasks, piv_type, oplist, herm, vev, rotop, piv_name, tmin, tmax, tnorm, tmet, tdiag, piv_file, rotcorr_file, plot_sampling, effenergytype, Eplotstub, Cplotstub, improved_op_logs=None):
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
        ET.SubElement(matrixinfo, getoptype(x)).text = x

    if herm:
        ET.SubElement(matrixinfo, "HermitianMatrix")
    if vev:
        ET.SubElement(matrixinfo, "SubtractVEV")

    if improved_op_logs != None:
        improved_ops = ET.SubElement(pivoter, "ImprovedOperators")
        if isinstance(improved_op_logs, basestring):
            parse_improved_ops_log(improved_ops, improved_op_logs)
        else:
            for log in improved_op_logs:
                parse_improved_ops_log(improved_ops, log)

    rotatedop = ET.SubElement(pivoter, "RotatedCorrelator")
    ET.SubElement(rotatedop, "GIOperatorString").text = rotop

    ET.SubElement(pivoter, "AssignName").text = piv_name
    ET.SubElement(pivoter, "NormTime").text = str(tnorm)
    ET.SubElement(pivoter, "MetricTime").text = str(tmet)
    ET.SubElement(pivoter, "DiagonalizeTime").text = str(tdiag)
    ET.SubElement(pivoter, "MinimumInverseConditionNumber").text = "0.01"
    ET.SubElement(pivoter, "NegativeEigenvalueAlarm").text = "-0.01"
    ET.SubElement(pivoter, "CheckMetricErrors")
    ET.SubElement(pivoter, "CheckCommonMetricMatrixNullSpace")
    ET.SubElement(pivoter, "PrintTransformationMatrix")

    writepiv = ET.SubElement(pivoter, "WritePivotToFile")
    ET.SubElement(writepiv, "PivotFileName").text = piv_file
    ET.SubElement(writepiv, "Overwrite")

    writecorr = ET.SubElement(task, "WriteRotatedCorrToFile")
    ET.SubElement(writecorr, "RotatedCorrFileName").text = rotcorr_file
    ET.SubElement(writecorr, "Type").text = "bins" # Or samplings?
    ET.SubElement(writecorr, "Overwrite")

    plots = ET.SubElement(task, "PlotRotatedEffectiveEnergies")
    ET.SubElement(plots, "SamplingMode").text = plot_sampling
    if any(effenergytype == x for x in ["TimeForward", "TimeForwardPlusConst", "TimeSymmetric", "TimeSymmetricPlusConst"]):
        ET.SubElement(plots, "EffEnergyType").text = effenergytype
    else:
        print("give a better eff energy type")
        sys.exit()

    ET.SubElement(plots, "TimeStep").text = "3"
    ET.SubElement(plots, "PlotFileStub").text = Eplotstub
    ET.SubElement(plots, "SymbolColor").text = "blue"
    ET.SubElement(plots, "SymbolType").text = "circle"
    ET.SubElement(plots, "MaxErrorToPlot").text = "1.0"

    corrplots = ET.SubElement(task, "PlotRotatedCorrelators")
    ET.SubElement(corrplots, "SamplingMode").text = plot_sampling
    ET.SubElement(corrplots, "PlotFileStub").text = Cplotstub
    ET.SubElement(corrplots, "Arg").text = "Re"
    ET.SubElement(corrplots, "SymbolColor").text = "blue"
    ET.SubElement(corrplots, "SymbolType").text = "circle"
    ET.SubElement(corrplots, "Rescale").text = "1.0"


# Insert fit energies and amplitudes into a pivot in memory or on file
def insertintopivot(tasks, piv_type, piv_name, energies, amps, piv_file=None, reorder=True):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoRotCorrMatInsertFitInfos"
    if piv_file is None:
        getpivot(task, piv_type, piv_name)
    else:
        readpivot(task, piv_type, piv_file, piv_name)

    if reorder:
        ET.SubElement(task, "ReorderByFitEnergy")

    if isinstance(energies, basestring):
        ET.SubElement(task, "EnergyFitCommonName").text = energies
    elif len(energies) == 1:
        ET.SubElement(task, "EnergyFitCommonName").text = energies[0][0]
    else:
        for level in energies:
            energy = ET.SubElement(task, "EnergyFit")
            ET.SubElement(energy, "Level").text = str(level[1])
            ET.SubElement(energy, "Name").text = level[0]
            ET.SubElement(energy, "IDIndex").text = str(level[1])

    if isinstance(amps, basestring):
        ET.SubElement(task, "RotatedAmplitudeCommonName").text = amps
    elif len(amps) == 1:
        ET.SubElement(task, "RotatedAmplitudeCommonName").text = amps[0][0]
    else:
        for level in amps:
            amp = ET.SubElement(task, "RotatedAmplitude")
            ET.SubElement(amp, "Level").text = str(level[1])
            ET.SubElement(amp, "Name").text = level[0]
            ET.SubElement(amp, "IDIndex").text = str(level[1])


# After levels have been reordered in a pivot, rename plot files for the reordered levels
def relabelplots(tasks, piv_type, piv_name, oldstub, piv_file=None, newstub=None):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoCorrMatrixRelabelEnergyPlots"
    if piv_file is None:
        getpivot(task, piv_type, piv_name)
    else:
        readpivot(task, piv_type, piv_file, piv_name)

    originals = ET.SubElement(task, "OriginalPlotFiles")
    if isinstance(oldstub, basestring):
        ET.SubElement(originals, "PlotFileStub").text = oldstub
    else:
        for x in oldstub:
            ET.SubElement(originals, "PlotFile").text = x

    if newstub is not None:
        revised = ET.SubElement(task, "RevisedPlotFiles")
        if isinstance(newstub, basestring):
            ET.SubElement(revised, "PlotFileStub").text = newstub
        elif len(newstub) == 1:
            ET.SubElement(revised, "PlotFileStub").text = newstub
        else:
            for x in newstub:
                ET.SubElement(revised, "PlotFile").text = x


# Calculate Z factors and produce plots from pivot and opstrings (fit amplitudes must already be in pivot)
def zfactors(tasks, piv_type, piv_name, plotstub, opstrings, piv_file=None):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoCorrMatrixZMagSquares"
    if piv_file is None:
        getpivot(task, piv_type, piv_name)
    else:
        readpivot(task, piv_type, piv_file, piv_name)

    plots = ET.SubElement(task, "DoPlots")
    ET.SubElement(plots, "PlotFileStub").text = plotstub
    ET.SubElement(plots, "BarColor").text = "cyan" # include option to pick/change this?

    for x in opstrings:
        zplot = ET.SubElement(plots, "ZMagSqPlot")
        ET.SubElement(zplot, getoptype(x)).text = x
        ET.SubElement(zplot, "ObsName").text = "standard"
        # ET.SubElement(zplot, "FileSuffix").text = uhh.. defaults to index. Maybe write something to get something from the OpString?


# Effective mass fit to UNROTATED correlator data
def dofit(tasks, operator, fitname, tmin, tmax, fitfn, minimizer, plotfile, psq, energies, refenergy, sampling, exclude="none", pivot="none", level="none"):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoFit"
    ET.SubElement(task, "Type").text = "TemporalCorrelator"

    minimizerinfo(task, minimizer)

    ET.SubElement(task, "SamplingMode").text = sampling
    ET.SubElement(task, "CovMatCalcSamplingMode").text = sampling

    fit = ET.SubElement(task, "TemporalCorrelatorFit")

    ET.SubElement(fit, getoptype(operator)).text = operator
    ET.SubElement(fit, "MinimumTimeSeparation").text = str(tmin)
    ET.SubElement(fit, "MaximumTimeSeparation").text = str(tmax)
    if(exclude != "none"):
        ET.SubElement(fit, "ExcludeTimes").text = exclude
    ET.SubElement(fit, "LargeTimeNoiseCutoff").text = "0.0"

    model = ET.SubElement(fit, "Model")
    ET.SubElement(model, "Type").text = fitfn

    fitmodel = shortform(fitfn)

    if(len(fitname) < 8):
        obsname = str(fitname) + "_" + str(tmin) + "_" + str(tmax) + "P" + str(psq) + fitmodel
    else:
        print("fitname: " + fitname + " may be too long for obsnames")
        sys.exit()

    energies.append("E1_" + obsname)
    modelparams(model, obsname)

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

    if pivot != "none":
        insert = ET.SubElement(fit, "InsertIntoPivot")
        ET.SubElement(insert, "Type").text = "Single" # Only single pivot implemented so far
        ET.SubElement(insert, "Name").text = str(pivot) # Object name, NOT filename. Must already be in memory
        ET.SubElement(insert, "Level").text = str(level)


# Effective mass fit to ROTATED correlator data
def dorotfit(tasks, operator_base, level, obsname, tmin, tmax, fitfn, minimizer, plotfile, psq, energies, amplitudes, refenergy, sampling, exclude="none", pivot="none"):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoFit"
    ET.SubElement(task, "Type").text = "TemporalCorrelator"

    minimizerinfo(task, minimizer)

    ET.SubElement(task, "SamplingMode").text = sampling
    ET.SubElement(task, "CovMatCalcSamplingMode").text = sampling

    fit = ET.SubElement(task, "TemporalCorrelatorFit")
    if operator_base[-1] == " ":
        operator = operator_base + str(level)
    else:
        operator = operator_base + " " + str(level)

    ET.SubElement(fit, getoptype(operator)).text = operator
    ET.SubElement(fit, "MinimumTimeSeparation").text = str(tmin)
    ET.SubElement(fit, "MaximumTimeSeparation").text = str(tmax)
    if(exclude != "none"):
        ET.SubElement(fit, "ExcludeTimes").text = exclude
    ET.SubElement(fit, "LargeTimeNoiseCutoff").text = "0.0"

    model = ET.SubElement(fit, "Model")
    ET.SubElement(model, "Type").text = fitfn

    fitmodel = shortform(fitfn)

    if(len(obsname) > 20):
        print("WARNING: obsname " + obsname + " may be too long for obsnames")

    energies.append(["E1_" + obsname, level])
    amplitudes.append(["A1_" + obsname, level])
    modelparams(model, obsname, level)

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

    if pivot != "none":
        insert = ET.SubElement(fit, "InsertIntoPivot")
        ET.SubElement(insert, "Type").text = "Single" # Only single pivot implemented so far
        ET.SubElement(insert, "Name").text = str(pivot) # Object name, NOT filename. Must already be in memory
        ET.SubElement(insert, "Level").text = str(level)


def writesamplings(tasks, energies, energyfile, sampling="Bootstrap", overwrite=True):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "WriteSamplingsToFile"
    ET.SubElement(task, "SamplingMode").text = sampling
    ET.SubElement(task, "FileName").text = energyfile
    if overwrite:
        ET.SubElement(task, "FileMode").text = "overwrite"

    for x in energies:
        obs = ET.SubElement(task, "MCObservable")
        if isinstance(x, basestring):
            ET.SubElement(obs, "ObsName").text = x
            ET.SubElement(obs, "Index").text = "0"
        elif len(x) == 2:
            ET.SubElement(obs, "ObsName").text = x[0]
            ET.SubElement(obs, "Index").text = str(x[1])
        else:
            print("Please give a better obsname format to write samplings")
            sys.exit()


def readsamplings(tasks, filename, sampling, mcobs):
    task = ET.SubElement(tasks, "Task")
    ET.SubElement(task, "Action").text = "ReadSamplingsFromFile"
    ET.SubElement(task, "SamplingMode").text = sampling
    ET.SubElement(task, "FileName").text = filename
    for x in mcobs:
        obs = ET.SubElement(task, "MCObservable")
        if isinstance(x, basestring):
            ET.SubElement(obs, "ObsName").text = x
            ET.SubElement(obs, "IDIndex").text = "0"
        elif len(x) == 2:
            ET.SubElement(obs, "ObsName").text = x[0]
            ET.SubElement(obs, "IDIndex").text = str(x[1])
        else:
            print("Please give a better obsname format to read samplings")
            sys.exit()


def diagonalenergyplots(tasks, oplist, filestub, sampling="Jackknife"):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoPlot"
    ET.SubElement(task, "Type").text = "EffectiveEnergies"
    ET.SubElement(task, "EffEnergyType").text = "TimeSymmetric" # flag for forward vs symmetric?
    ET.SubElement(task, "TimeStep").text = "3"

    corrset = ET.SubElement(task, "DiagonalCorrelatorSet")
    seq = ET.SubElement(corrset, "Sequential")
    for x in oplist:
        ET.SubElement(seq, "BLOperatorString").text = x

    ET.SubElement(task, "Sampling").text = sampling
    ET.SubElement(task, "PlotFileStub").text = filestub
    ET.SubElement(task, "CorrName").text = "standard"


def diagonalcorrelatorplots(tasks, oplist, filestub, sampling="Jackknife", herm=True, subVEV=False):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoPlot"
    ET.SubElement(task, "Type").text = "TemporalCorrelators"

    corrset = ET.SubElement(task, "DiagonalCorrelatorSet")
    seq = ET.SubElement(corrset, "Sequential")
    for x in oplist:
        ET.SubElement(seq, "BLOperatorString").text = x

    if herm:
        ET.SubElement(task, "HermitianMatrix")
    if subVEV:
        ET.SubElement(task, "SubtractVEV")

    ET.SubElement(task, "Sampling").text = sampling
    ET.SubElement(task, "PlotFileStub").text = filestub


# Average correlators of equivalent total momentum. (For now assumes all coeffs = 1.0)
def momaverage(tasks, oplists, psq, binfile, tmin, tmax, hermitian=True):
    task = ET.SubElement(tasks, "Task")
    ET.SubElement(task, "Action").text = "DoObsFunction"
    ET.SubElement(task, "Type").text = "CorrelatorMatrixSuperposition"
    results = ET.SubElement(task, "ResultOperatorOrderedList")

    result_strs = []
    FLAV_MAP = {
        'eta': 'singlet',
        'phi': 'singlet',
        'lambda': 'singlet',
        'omega': 'singlet',
        'kaon': 'doublet',
        'kbar': 'doublet',
        'nucleon': 'doublet',
        'xi': 'doublet',
        'pion': 'triplet',
        'sigma': 'triplet',
        'delta': 'quartet'
        }
    MOM_MAP = {
        0: 'P=(0,0,0)',
        1: 'P=(0,0,1)',
        2: 'P=(0,1,1)',
        3: 'P=(1,1,1)',
        4: 'P=(0,0,2)',
        5: 'P=(0,1,2)',
        6: 'P=(1,1,2)'
        }

    # Get GI opstring from oplists
    for op in oplists[0]:
        if "iso" not in op.split()[0]: # if SH op
            result_strs.append('iso' + FLAV_MAP[op.split()[0]] + ' ' + MOM_MAP[psq] + ' '
                               + op.split()[2] + ' ' + op.split()[0].upper() + '_' + op.split()[3])
        else:
            result_strs.append(op.split('_')[0] + ' ' + MOM_MAP[psq] + ' ' + op.split()[1] + ' '
                               + op.split('_')[1].upper() + '_' + op.split()[3] + '_' + op.split('_')[2].upper().split()[0] + '_' + op.split()[6])

    # GIOperatorStrings for resultant averaged matrix here
    for opname in result_strs:
        ET.SubElement(results, "GIOperatorString").text = opname

    for oplist in oplists:
        matrix = ET.SubElement(task, "OperatorOrderedList")
        for opname in oplist:
            item = ET.SubElement(matrix, "Item")
            ET.SubElement(item, "BLOperatorString").text = opname
            ET.SubElement(item, "Coefficient").text = "1.0"

    ET.SubElement(task, "MinimumTimeSeparation").text = str(tmin)
    ET.SubElement(task, "MaximumTimeSeparation").text = str(tmax)
    if(hermitian):
        ET.SubElement(task, "HermitianMatrix")
    ET.SubElement(task, "WriteToBinFile").text = binfile
    ET.SubElement(task, "FileMode").text = "overwrite"

    return result_strs


# Momentum average operators based on opdefs file. This is depricated and will only work for data from the 'special' directories
def momaverage_opdefs(tasks, opfile, psq, binfile, tmin, tmax, hermitian=True):
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

    # associate GI or BL with each operator? -- check for isospin or flavour -- fix this with getoptype fn
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

    minimizerinfo(task, minimizer)

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


def add_obs(tasks, obs_strs, result_str, mode, single=False):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoObsFunction"
    ET.SubElement(task, "Type").text = "LinearSuperposition"

    result = ET.SubElement(task, "Result")
    ET.SubElement(result, "Name").text = result_str
    ET.SubElement(result, "IDIndex").text = "0"

    if not single:
        for x in obs_strs:
            summand = ET.SubElement(task, "Summand")
            obs = ET.SubElement(summand, "MCObservable")
            ET.SubElement(obs, "ObsName").text = x
            ET.SubElement(obs, "Index").text = "0"
            ET.SubElement(summand, "Coefficient").text = "1.0"
    else:
        summand = ET.SubElement(task, "Summand")
        obs = ET.SubElement(summand, "MCObservable")
        ET.SubElement(obs, "ObsName").text = obs_strs[0]
        ET.SubElement(obs, "Index").text = "0"
        ET.SubElement(summand, "Coefficient").text = "1.0"
        summand = ET.SubElement(task, "Summand")
        obs = ET.SubElement(summand, "MCObservable")
        ET.SubElement(obs, "ObsName").text = obs_strs[1]
        ET.SubElement(obs, "Index").text = "0"
        ET.SubElement(summand, "Coefficient").text = "0.0"

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


def corr_timediff(tasks, oplist, tmin, tmax, filename="none", hermitian=True, overwrite=True):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoObsFunction"
    ET.SubElement(task, "Type").text = "CorrelatorMatrixTimeDifferences"

    newlist = ET.SubElement(task, "NewOperatorOrderedList")
    for x in oplist:
        ET.SubElement(newlist, "GIOperatorString").text = getTsubopstring(x)

    oldlist = ET.SubElement(task, "OldOperatorOrderedList")
    for x in oplist:
        ET.SubElement(oldlist, getoptype(x)).text = x

    ET.SubElement(task, "MinimumTimeSeparation").text = str(tmin)
    ET.SubElement(task, "MaximumTimeSeparation").text = str(tmax)
    if hermitian:
        ET.SubElement(task, "HermitianMatrix")
    if filename != "none":
        ET.SubElement(task, "WriteToBinFile").text = filename
    if overwrite:
        ET.SubElement(task, "FileMode").text = "overwrite"


# Effective mass fits to two single real-valued correlators -- ratio or something?
def dodoublefit(tasks, op1, op2, fitname1, fitname2, tmin1, tmax1, tmin2, tmax2, fitfn1, fitfn2, minimizer, plotfile, psq1, psq2, ratio_name, energies, sampling, exclude1="none", exclude2="none", pivot="none", level="none"):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoFit"
    ET.SubElement(task, "Type").text = "TwoTemporalCorrelator"

    minimizerinfo(task, minimizer)

    ET.SubElement(task, "SamplingMode").text = sampling
    ET.SubElement(task, "CovMatCalcSamplingMode").text = sampling

    fit = ET.SubElement(task, "TwoTemporalCorrelatorFit")

    # Correlator 1
    corr1 = ET.SubElement(fit, "CorrelatorOne")
    ET.SubElement(corr1, getoptype(op1)).text = op1
    ET.SubElement(corr1, "MinimumTimeSeparation").text = str(tmin1)
    ET.SubElement(corr1, "MaximumTimeSeparation").text = str(tmax1)
    if(exclude1 != "none"):
        ET.SubElement(corr1, "ExcludeTimes").text = exclude1
    ET.SubElement(corr1, "LargeTimeNoiseCutoff").text = "1.0"

    model = ET.SubElement(corr1, "Model")
    ET.SubElement(model, "Type").text = fitfn1

    fitmodel = shortform(fitfn1)

    if(len(fitname1) < 8):
        obsname = str(fitname1) + "_" + str(tmin1) + "_" + str(tmax1) + "P" + str(psq1) + fitmodel
    else:
        print("fitname1: " + fitname1 + " may be too long for obsnames")
        sys.exit()

    energies.append("E1_" + obsname)
    modelparams(model, obsname)

    # Correlator 2
    corr2 = ET.SubElement(fit, "CorrelatorTwo")
    ET.SubElement(corr2, getoptype(op2)).text = op2
    ET.SubElement(corr2, "MinimumTimeSeparation").text = str(tmin2)
    ET.SubElement(corr2, "MaximumTimeSeparation").text = str(tmax2)
    if(exclude2 != "none"):
        ET.SubElement(corr2, "ExcludeTimes").text = exclude2
    ET.SubElement(corr2, "LargeTimeNoiseCutoff").text = "1.0"

    model = ET.SubElement(corr2, "Model")
    ET.SubElement(model, "Type").text = fitfn2

    fitmodel = shortform(fitfn2)

    if(len(fitname2) < 8):
        obsname = str(fitname2) + "_" + str(tmin2) + "_" + str(tmax2) + "P" + str(psq2) + fitmodel
    else:
        print("fitname2: " + fitname2 + " may be too long for obsnames")
        sys.exit()

    energies.append("E1_" + obsname)
    modelparams(model, obsname)

    # Energy Ratio
    rat = ET.SubElement(fit, "EnergyRatio")
    ET.SubElement(rat, "Name").text = ratio_name
    ET.SubElement(rat, "IDIndex").text = "0"

    plot = ET.SubElement(fit, "DoEffectiveEnergyPlot")
    ET.SubElement(plot, "PlotFile").text = plotfile
    ET.SubElement(plot, "CorrName").text = "standard"
    ET.SubElement(plot, "TimeStep").text = "3"
    ET.SubElement(plot, "SymbolColor").text = "blue"
    ET.SubElement(plot, "SymbolType").text = "circle"
    ET.SubElement(plot, "Goodness").text = "chisq"
    ET.SubElement(plot, "ShowApproach")

    if pivot != "none":
        insert = ET.SubElement(fit, "InsertIntoPivot")
        ET.SubElement(insert, "Type").text = "Single" # Only single pivot implemented so far
        ET.SubElement(insert, "Name").text = str(pivot) # Object name, NOT filename. Must already be in memory
        ET.SubElement(insert, "Level").text = str(level)
