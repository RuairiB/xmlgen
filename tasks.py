import xml.etree.cElementTree as ET
import os

# SigMond tasks
# Tasks To Do:
# -> DoPlot - all
# -> DoObs - all
# -> Memory management
# -> Reading/Writing to file
# -> PrintXML - all
#
# Rewrite to allow for operator lists instead of Corr matrix name?

# Read in (usually rotated) bins from file
def readbins(tasks, binfile):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "ReadBinsFromFile"
    ET.SubElement(task, "FileName").text = binfile


# Old SigMond rotation inputs; routines need to be run separately for some unknown reason...
def oldrotateA(tasks, mintime, maxtime, proj_name, file_tail, norm_time, metric_time, diag_time, cond_num):
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

def oldrotateB(tasks, mintime, maxtime, proj_name, file_tail):
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


# Effective mass fit to (rotated) correlator data
def dofit(tasks, proj_name, level, tmin, tmax, fitfn, plotfile, plotname, sampling="Bootstrap"):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoCorrMatrixRotation"
    ET.SubElement(task, "Type").text = "TemporalCorrelator"
    
    mini = ET.SubElement(task, "MinimizerInfo")
    ET.SubElement(mini, "Method").text = "Minuit2"
    ET.SubElement(mini, "ParameterRelTol").text = "1e-6"
    ET.SubElement(mini, "ChiSquareRelTol").text = "1e-4"
    ET.SubElement(mini, "MaximumIterations").text = "1024"
    ET.SubElement(mini, "Verbosity").text = "Low"

    ET.SubElement(task, "SamplingMode").text = sampling

    fit = ET.SubElement(task, "TemporalCorrelatorFit")
    
    op = ET.SubElement(fit, "RotatedOperator")
    ET.SubElement(op, "ObsName").text = "proj_name"
    ET.SubElement(op, "Level").text = str(level)

    ET.SubElement(fit, "MinimumTimeSeparation").text = str(tmin)
    ET.SubElement(fit, "MaximumTimeSeparation").text = str(tmax)
    ET.SubElement(fit, "LargeTimeNoiseCutoff").text = "1.0"

    model = ET.SubElement(fit, "Model")
    ET.SubElement(model, "Type").text = fitfn

    eng = ET.SubElement(model, "Energy")
    ET.SubElement(eng, "Name").text = "FitSE"
    ET.SubElement(eng, "IDIndex").text = "0"
    amp = ET.SubElement(model, "Amplitude")
    ET.SubElement(amp, "Name").text = "A0SE"
    ET.SubElement(amp, "IDIndex").text = "0"
    eng1 = ET.SubElement(model, "FirstEnergy")
    ET.SubElement(eng1, "Name").text = "FitTE"
    ET.SubElement(eng1, "IDIndex").text = "0"
    amp1 = ET.SubElement(model, "FirstAmplitude")
    ET.SubElement(amp1, "Name").text = "A0TE"
    ET.SubElement(amp1, "IDIndex").text = "0"
    eng2 = ET.SubElement(model, "SqrtGapToSecondEnergy")
    ET.SubElement(eng2, "Name").text = "FitGapTE"
    ET.SubElement(eng2, "IDIndex").text = "0"
    amp2 = ET.SubElement(model, "SecondAmplitudeRatio")
    ET.SubElement(amp2, "Name").text = "A1TE"
    ET.SubElement(amp2, "IDIndex").text = "0"
    const = ET.SubElement(model, "AddedConstant")
    ET.SubElement(const, "Name").text = "C"
    ET.SubElement(const, "IDIndex").text = "0"

    plot = ET.SubElement(fit, "DoEffectiveEnergyPlot")
    ET.SubElement(plot, "PlotFile").text = plotfile
    ET.SubElement(plot, "CorrName").text = plotname
    ET.SubElement(plot, "TimeStep").text = "3"
    ET.SubElement(plot, "SymbolColor").text = "blue"
    ET.SubElement(plot, "SymbolType").text = "circle"
    ET.SubElement(plot, "Goodness").text = "chisq"
    ET.SubElement(plot, "ShowApproach")


# Check correlator data for outliers, zeros in the correlator
def dochecks_outliers(tasks, mintime, maxtime, proj_name, scale=20):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoChecks"
    ET.SubElement(task, "Type").text = "TemporalCorrelatorMatrix"

    corr = ET.SubElement(task, "CorrelatorMatrixInfo")
    ET.SubElement(corr, "Name").text = proj_name

    ET.SubElement(task, "MinTimeSep").text = str(mintime)
    ET.SubElement(task, "MaxTimeSep").text = str(maxtime)
    ET.SubElement(task, "OutlierScale").text = str(scale)
    ET.SubElement(task, "Verbose")

    
# Check correlator data for hermiticity
def dochecks_hermitian(tasks, mintime, maxtime, proj_name):
    task = ET.SubElement(tasks, "Task")

    ET.SubElement(task, "Action").text = "DoChecks"
    ET.SubElement(task, "Type").text = "TemporalCorrelatorMatrixIsHermitian"

    corr = ET.SubElement(task, "CorrelatorMatrixInfo")
    ET.SubElement(corr, "Name").text = proj_name

    ET.SubElement(task, "MinTimeSep").text = str(mintime)
    ET.SubElement(task, "MaxTimeSep").text = str(maxtime)
    ET.SubElement(task, "Verbose")
