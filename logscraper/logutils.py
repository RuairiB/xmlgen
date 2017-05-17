import xml.etree.cElementTree as ET
import os
import sys
import math

def texfig(fig, filename, fit):
    f = open(filename + ".tex", 'w')

    f.write("\\begin{figure}\n")
    f.write("\\centering\n")
    f.write("\\includegraphics[scale=1]{" + fig + "}\n")
    f.write("\\caption{Fit to " + fit.opstring_tex + " for $t_{\\mathrm{min}} = " + fit.tmin + "$, $t_{\\mathrm{max}} = " + fit.tmax + "$ with \\vb{" + fit.model + "} fit model and " + fit.sampling + " resampling}\n")
    f.write("\\end{figure}\n")
    f.close()

def textable_fits(fits, psq, sampling, filename):
    # pull out desired psq & sampling
    table = []
    for i in fits:
        if i.psq == psq and i.sampling == str(sampling):
            if float(i.chisq) < 5.0:
                table.append(i)

    if table:
        # open output tex file
        f = open(filename + ".tex", 'w')

        # print header, environment, hlines, etc
        # f.write("\\begin{table}[h]\n")
        # f.write("\\centering\n")
        # f.write("\\begin{tabular}{| c | c | c | c | c |}\n")
        f.write("\\begin{longtable}{| c | c | c | c | c |}\n")
        f.write("\\hline\n")
        f.write("Fit Type & $t_{\\mathrm{min}}$ & $t_{\\mathrm{max}}$ & $a_t E_{\\mathrm{fit}}$ & $\\chi^2$ \\\\\n")
        f.write("\\hline\n")

        # split by fit model -- add time forward
        tableTSSE = [x for x in table if x.model == "TimeSymSingleExponential"]
        tableTSSEC = [x for x in table if x.model == "TimeSymSingleExponentialPlusConstant"]
        tableTSTE = [x for x in table if x.model == "TimeSymTwoExponential"]
        tableTSTEC = [x for x in table if x.model == "TimeSymTwoExponentialPlusConstant"]
        tableTSGS = [x for x in table if x.model == "TimeSymGeomSeriesExponential"]

        # print out table content
        if tableTSSE:
            tableTSSE.sort(key=lambda k: (int(k.tmax), int(k.tmin)))
            f.write("1-exp & " + tableTSSE[0].tmin + " & " + tableTSSE[0].tmax + " & " + tableTSSE[0].fitprint + " & " + tableTSSE[0].chisq + " \\\\ \n")
            for x in tableTSSE[1:]:
                f.write(" & " + x.tmin + " & " + x.tmax + " & " + x.fitprint + " & " + x.chisq + " \\\\ \n")

        if tableTSSEC:
            f.write("\\hline\n")
            tableTSSEC.sort(key=lambda k: (int(k.tmax), int(k.tmin)))
            f.write("1-exp + C & " + tableTSSEC[0].tmin + " & " + tableTSSEC[0].tmax + " & " + tableTSSEC[0].fitprint + " & " + tableTSSEC[0].chisq + " \\\\ \n")
            for x in tableTSSEC[1:]:
                f.write(" & " + x.tmin + " & " + x.tmax + " & " + x.fitprint + " & " + x.chisq + " \\\\ \n")

        if tableTSTE:
            f.write("\\hline\n")
            tableTSTE.sort(key=lambda k: (int(k.tmax), int(k.tmin)))
            f.write("2-exp & " + tableTSTE[0].tmin + " & " + tableTSTE[0].tmax + " & " + tableTSTE[0].fitprint + " & " + tableTSTE[0].chisq + " \\\\ \n")
            for x in tableTSTE[1:]:
                f.write(" & " + x.tmin + " & " + x.tmax + " & " + x.fitprint + " & " + x.chisq + " \\\\ \n")

        if tableTSTEC:
            f.write("\\hline\n")
            tableTSTEC.sort(key=lambda k: (int(k.tmax), int(k.tmin)))
            f.write("2-exp + C & " + tableTSTEC[0].tmin + " & " + tableTSTEC[0].tmax + " & " + tableTSTEC[0].fitprint + " & " + tableTSTEC[0].chisq + " \\\\ \n")
            for x in tableTSTEC[1:]:
                f.write(" & " + x.tmin + " & " + x.tmax + " & " + x.fitprint + " & " + x.chisq + " \\\\ \n")

        if tableTSGS:
            f.write("\\hline\n")
            tableTSGS.sort(key=lambda k: (int(k.tmax), int(k.tmin)))
            f.write("gs-exp & " + tableTSGS[0].tmin + " & " + tableTSGS[0].tmax + " & " + tableTSGS[0].fitprint + " & " + tableTSGS[0].chisq + " \\\\ \n")
            for x in tableTSGS[1:]:
                f.write(" & " + x.tmin + " & " + x.tmax + " & " + x.fitprint + " & " + x.chisq + " \\\\ \n")

        # print bottom hline, end environment, etc
        f.write("\\hline\n")
        f.write("\\caption{Various fits to the " + table[0].opstring_tex + " operator on the \\vb{" + table[0].ensemble + "} ensemble with " + table[0].sampling + " sampling.}\n")
        f.write("\\end{longtable}\n")
        # f.write("\\end{tabular}\n")
        # f.write("\\caption{Various fits to the " + table[0].opstring_tex + " operator}\n")
        # f.write("\\end{table}\n")
        f.close()

        

def bestfit(fits, flav, psq, sampling, ensem):
    # determine 'best' fit from given list of fits for given psq & sampling mode
    # 'best' determined by chi^2 (and error?)
    wanted_fits = []
    for i in fits:
        if i.psq == psq and i.sampling == str(sampling) and i.flav == flav:
            wanted_fits.append(i)

    if ensem == "32_860":
        fudge = ["E1_kaon_4_35P0tsgs",
                 "E1_kaon_5_34P1tsgs",
                 "E1_kaon_5_35P2tsgs",
                 "E1_kaon_5_35P3tsgs",
                 "E1_kaon_4_35P4tsgs",
                 "E1_pion_3_35P0tsgs",
                 "E1_pion_4_35P1tsgs",
                 "E1_pion_4_35P2tsgs",
                 "E1_pion_4_35P3tsgs",
                 "E1_pion_4_35P4tsgs",
                 "E1_nucleon_3_24P0tste",
                 "E1_nucleon_3_25P1tsgs",
                 "E1_nucleon_3_25P2tsgs",
                 "E1_nucleon_4_25P3tste",
                 "E1_nucleon_3_25P4tsgs",
                 "E1_eta_17_24P0tsseC",
                 "E1_eta_17_24P1tsseC",
                 "E1_eta_17_25P2tsseC",
                 "E1_eta_17_25P3tsse",
                 "E1_eta_17_25P4tsse"]
    elif ensem == "24_840":
        fudge = ["E1_kaon_4_35P0tsgs",
                 "E1_kaon_4_35P1tsgs",
                 "E1_kaon_4_35P2tsgs",
                 "E1_kaon_4_35P3tsgs",
                 "E1_kaon_3_35P4tsgs",
                 "E1_pion_4_35P0tsgs",
                 "E1_pion_4_35P1tsgs",
                 "E1_pion_4_35P2tsgs",
                 "E1_pion_3_35P3tsgs",
                 "E1_pion_4_35P4tsgs",
                 "E1_nucleon_3_25P0tsgs",
                 "E1_nucleon_3_25P1tsgs",
                 "E1_nucleon_3_25P2tsgs",
                 "E1_nucleon_3_25P3tsgs",
                 "E1_nucleon_3_25P4tsgs",
                 "E1_eta_17_25P0tsseC",
                 "E1_eta_17_25P1tsseC",
                 "E1_eta_17_25P2tsseC",
                 "E1_eta_17_25P3tsseC"]
    else:
        print("give better ensemble for best fit")
        sys.exit()

    if wanted_fits:
        temp = [x for x in wanted_fits if x.fitname in fudge]
        return temp[0]
            # 'best' fit by chi^2 closest to 1 -- worthless way to pick best fit
            # return min(wanted_fits, key=lambda x:abs(float(x.chisq_full) - 1))
    else:
        print("something is empty for " + flav + fits[0].ensemble + "  " + psq + "  " + sampling)
        # sys.exit()

def twopart_fitname(fits, samp):
    if(type(fits) != tuple):
        print("gis a tuple please")
        sys.exit()
    elif(len(fits) != 2):
        print("wrong tuple length")
        sys.exit()

    name = fits[0].flav + "_" + fits[1].flav + "_"
    name += fits[0].mom.replace(",", "") + "_" + fits[1].mom.replace(",", "")

    if samp == "Bootstrap":
        name += "_boot"
        return name
    elif samp == "Jackknife":
        name += "_jack"
        return name
    elif samp == "none":
        return name
    else:
        print("wrong sampling")
        sys.exit()

def threepart_fitname(fits, samp):
    if(type(fits) != tuple):
        print("gis a tuple please")
        sys.exit()
    elif(len(fits) != 3):
        print("wrong tuple length")
        sys.exit()

    name = fits[0].flav + "_" + fits[1].flav + "_" + fits[2].flav + "_"
    # name += fits[0].mom.replace(",", "") + fits[1].mom.replace(",", "") + fits[2].mom.replace(",", "")
    name += fits[0].psq + "_" + fits[1].psq + "_" + fits[2].psq

    if samp == "Bootstrap":
        name += "boot"
        return name
    elif samp == "Jackknife":
        name += "jack"
        return name
    elif samp == "none":
        return name
    else:
        print("wrong sampling")
        sys.exit()


class fitlog:
    def psqfromstring(self):
        mom0 = ["0,0,0"]
        mom1 = ["0,0,1", "0,0,-1", "0,1,0", "0,-1,0", "1,0,0", "-1,0,0"]
        mom2 = ["0,1,1", "0,-1,1", "0,1,-1", "0,-1,-1", "1,0,1", "1,0,-1", "-1,0,1", "-1,0,-1", "1,1,0", "1,-1,0", "-1,1,0", "-1,-1,0"]
        mom3 = ["1,1,1", "1,1,-1", "1,-1,1", "-1,1,1", "-1,-1,1", "-1,1,-1", "1,-1,-1", "-1,-1,-1"]
        mom4 = ["0,0,2", "0,0,-2", "0,2,0", "0,-2,0", "2,0,0", "-2,0,0"]
        mom5 = ["1,2,0", "-1,0,-2", "-1,0,2", "-1,2,0", "-2,-1,0", "-2,0,-1", "-2,0,1", "-2,1,0", "0,-1,-2", "0,-1,2", "0,-2,-1", "0,-2,1", "2,1,0", "2,0,1", "2,0,-1", "2,-1,0", "-1,-2,0", "1,0,2", "1,0,-2", "1,-2,0", "0,2,1", "0,1,2", "0,2,-1", "0,1,-2"]
        mom6 = ["1,1,2", "-1,-2,-1", "-1,-2,1", "-1,1,-2", "-1,1,2", "-1,-1,-2", "-1,2,-1", "-1,2,1", "-2,-1,-1", "-2,-1,1", "-2,1,-1", "-2,1,1", "1,-1,-2", "1,-1,2", "1,-2,-1", "1,-2,1", "1,1,-2", "-1,-1,2", "1,2,-1", "1,2,1", "2,-1,-1", "2,-1,1", "2,1,-1", "2,1,1"]
        if any(x in self.opstring for x in mom0):
            self.psq = "0"
            self.mom = next((y for y in mom0 if y in mom0), False)
        elif any(x in self.opstring for x in mom1):
            self.psq = "1"
            self.mom = next((y for y in mom1 if y in mom1), False)
        elif any(x in self.opstring for x in mom2):
            self.psq = "2"
            self.mom = next((y for y in mom2 if y in mom2), False)
        elif any(x in self.opstring for x in mom3):
            self.psq = "3"
            self.mom = next((y for y in mom3 if y in mom3), False)
        elif any(x in self.opstring for x in mom4):
            self.psq = "4"
            self.mom = next((y for y in mom4 if y in mom4), False)
        elif any(x in self.opstring for x in mom5):
            self.psq = "5"
            self.mom = next((y for y in mom5 if y in mom5), False)
        elif any(x in self.opstring for x in mom6):
            self.psq = "6"
            self.mom = next((y for y in mom6 if y in mom6), False)
        else:
            print("Couldn't determine operator momentum")

    def psqfromfitname(self):
        self.psq = self.fitname.split("P")[1]
        self.psq = self.psq[:1]
        
    # Combine error formatting and sig fig cut offs into one function -- comment this better...
    def sigfigs(self, err_nprec):
        self.chisq_full = self.chisq
        self.chisq = str(format(float(self.chisq), '.2f'))

        if self.fiterr != "0":
            zeros = math.ceil(abs(math.log10(float(self.fiterr)))) - 1
            self.fiterr_zeros = zeros
            # strip non zero part of error (& e-05, etc) and pull out first two non zero bits (rounded)
            err_decimal = self.fiterr.split(".", 1)[1].lstrip("0").split("e", 1)[0] 
            err_print = str(round(float(err_decimal[:3]), -1))[:2]

            # truncate fit energy & add error
            self.fitprint = self.fitenergy[:2+int(zeros)+err_nprec] + "(" + err_print + ")"
        else:
            self.fitprint = self.fitenergy[:2+err_nprec] + "(" + self.fiterr + ")"
        
            
    # put octahedral irrep and displacement into latex math mode
    def texopstring(self):
        self.opstring = self.opstring.replace("_0 0", "_0")
        self.opstring = self.opstring.replace("_1 0", "_1")
        # self.opstring = self.opstring.replace("_1", "")
        # self.opstring = self.opstring.replace("_2", "")
        # self.opstring_tex = self.opstring.split(")", 1)[0] + ") $" + self.opstring.split(") ", 1)[1] + "$"
        self.opstring_tex = "\\vb{" + self.opstring.replace('_', '\\_') + "}"

    def texensemble(self):
        self.ensemble = self.ensemble.replace('_', '\\_')
        
    def stripindex(self):
        self.fitname = self.fitname.split(" Index", 1)[0]
        self.xistring = self.xistring.split(" Index", 1)[0]

    def findplot(self):
        i = self
        if "32" in i.ensemble:
            ensem = "32"
            ensem2 = "32_860"
        elif "24" in i.ensemble:
            ensem = "24"
            ensem2 = "24_840"
        else:
            print("something is going bad, can't find ensemble")
            sys.exit()

        if i.model == "TimeSymSingleExponential":
            fitfn = "tsse"
        elif i.model == "TimeForwardSingleExponential":
            fitfn = "tsse"
        elif i.model == "TimeSymSingleExponentialPlusConstant":
            fitfn = "tsseC"
        elif i.model == "TimeForwardSingleExponentialPlusConstant":
            fitfn = "tsseC"
        elif i.model == "TimeSymTwoExponential":
            fitfn = "tste"
        elif i.model == "TimeForwardTwoExponential":
            fitfn = "tste"
        elif i.model == "TimeSymTwoExponentialPlusConstant":
            fitfn = "tsteC"
        elif i.model == "TimeForwardTwoExponentialPlusConstant":
            fitfn = "tsteC"
        elif i.model == "TimeSymGeomSeriesExponential":
            fitfn = "tsgs"
        elif i.model == "TimeForwardGeomSeriesExponential":
            fitfn = "tsgs"
        else:
            print("no model found for " + i.model)
            sys.exit()

        if i.sampling == "Bootstrap":
            samp = "boot"
        elif i.sampling == "Jackknife":
            samp = "jack"
        else:
            print("no sampling info found")
            sys.exit()

        self.plotlocation = "/home/ruairi/research/freeparticle_energies/SH_fits/" + ensem + "^3/" + i.flav + "/fits/PSQ" + i.psq + "/pdfs/" + i.flav + "_" + ensem2 + "_PSQ" + i.psq + "_" + fitfn + "_tmin" + i.tmin + "tmax" + i.tmax + "_" + samp + ".pdf"


    def findflav(self, xi=False):
        if xi != True:
            if any(flav in self.opstring for flav in ["pion", "isotriplet"]):
                self.flav = "pion"
            elif any(flav in self.opstring for flav in ["G1g_", "G1_", "G_"]):
                self.flav = "nucleon"
            elif any(flav in self.opstring for flav in ["kaon", "A1_", "A2_"]):
                self.flav = "kaon"
            elif any(flav in self.opstring for flav in ["eta", "isosinglet"]):
                self.flav = "eta"
            else:
                print("Unknown operator flavour")
                sys.exit()
        else:
            if "pion" in self.xistring:
                self.flav = "pion"
            elif "nucleon" in self.xistring:
                self.flav = "nucleon"
            elif "kaon" in self.xistring:
                self.flav = "kaon"
            elif "eta" in self.xistring:
                self.flav = "eta"
            else:
                print("Unknown xi fit flavour")
                sys.exit()            

    def findflavfitname(self):
        if "pion" in self.fitname:
            self.flav = "pion"
        elif "nucleon" in self.fitname:
            self.flav = "nucleon"
        elif "kaon" in self.fitname:
            self.flav = "kaon"
        elif "eta" in self.fitname:
            self.flav = "eta"
        else:
            print("Unknown fit flavour")
            sys.exit()            


    def __init__(self):
        self.ensemble = ''
        self.opstring = ''
        self.opstring_tex = ''
        self.flav = ''
        self.psq = ''
        self.mom = ''
        self.tmin = ''
        self.tmax = ''
        self.model = ''
        self.chisq = ''
        self.chisq_full = ''
        self.fitname = ''
        self.fitenergy = ''
        self.fiterr_zeros = ''
        self.fiterr = ''
        self.fitprint = ''
        self.sampling = ''
        self.plotlocation = ''
        self.xistring = ''
        self.bestparams = False

        
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def textable_super(particles, psq, ensem, sampling, filename):
    # pull out desired ensemble & sampling
    table = []
    for i in particles:
        if ensem in i.ensemble and i.sampling == str(sampling) and i.psq == psq:
            table.append(i)

    if table:
        # open output tex file
        f = open(filename + ".tex", 'w')

        # print header, environment, hlines, etc
        f.write("\\begin{longtable}{| c || c | c |}\n")
        f.write("\\hline\n")
        f.write("Particle content & $a_t E$ & $\\frac{E}{m_K}$ \\\\\n")
        f.write("\\hline\n")

        # print out table content
        for x in table:
            f.write("$" + x.resultstr_tex + "$ & " + x.energyprint + " & " + x.energyratioprint + " \\\\ \n")

        
        # print bottom hline, end environment, etc
        f.write("\\hline\n")
        f.write("\\captionsetup{justification=centering}\n")
        f.write("\\caption{Two particle non-interacting energies with total momentum $P^2 = " + table[0].psq + "$ on the \\vb{" + table[0].ensemble + "} ensemble with " + table[0].sampling + " resampling.}\n")
        f.write("\\end{longtable}\n")
        f.close()    
        

        
class linsuperlog:
    def stripindex(self):
        self.resultstr = self.resultstr.split(" Index", 1)[0]
        self.ratio_str = self.ratio_str.split(" Index", 1)[0]

    def texensemble(self):
        self.ensemble = self.ensemble.replace('_', '\\_')
        
    # Combine error formatting and sig fig cut offs into one function -- comment this better...
    def sigfigs(self, err_nprec):
        zeros = math.ceil(abs(math.log10(float(self.energyerr)))) - 1
        self.energyerr_zeros = zeros
        # strip non zero part of error (& e-05, etc) and pull out first two non zero bits (rounded)
        err_decimal = self.energyerr.split(".", 1)[1].lstrip("0").split("e", 1)[0] 
        err_print = str(round(float(err_decimal[:3]), -1))[:2]

        # truncate fit energy & add error
        self.energyprint = self.energy[:2+int(zeros)+err_nprec] + "(" + err_print + ")"

        if self.energyratio != "":
            zeros = math.ceil(abs(math.log10(float(self.energyratioerr)))) - 1
            # strip non zero part of error (& e-05, etc) and pull out first two non zero bits (rounded)
            err_decimal = self.energyratioerr.split(".", 1)[1].lstrip("0").split("e", 1)[0] 
            err_print = str(round(float(err_decimal[:3]), -1))[:2]

            # truncate fit energy & add error
            self.energyratioprint = self.energyratio[:2+int(zeros)+err_nprec] + "(" + err_print + ")"

        
    # Flava flav has gone missing, can you find him?
    def findflav(self, num=2):
        self.flav1 = self.resultstr.split("_")[0]
        self.flav2 = self.resultstr.split("_")[1]
        if not any(x in self.flav1 for x in ("pion", "kaon", "eta", "nucleon")):
            print("what flavour are you particle 1?")
        if not any(x in self.flav2 for x in ("pion", "kaon", "eta", "nucleon")):
            print("what flavour are you particle 2?")

        if num > 2:
            self.flav3 = self.resultstr.split("_")[2]
            if not any(x in self.flav3 for x in ("pion", "kaon", "eta", "nucleon")):
                print("what flavour are you particle 3?")

        if num > 3:
            self.flav4 = self.resultstr.split("_")[3]
            if not any(x in self.flav4 for x in ("pion", "kaon", "eta", "nucleon")):
                print("what flavour are you particle 4?")

    # Where is she?
    def findmom(self, num=2):
        # perform some sort of check to make sure a momentum (rather than flav, etc) has been extracted
        if num == 2:
            self.mom1 = self.resultstr.split("_")[2]
            self.mom2 = self.resultstr.split("_")[3]
        if num == 3:
            self.mom1 = self.resultstr.split("_")[3]
            self.mom2 = self.resultstr.split("_")[4]
            self.mom3 = self.resultstr.split("_")[5]
        elif num == 4:
            self.mom1 = self.resultstr.split("_")[4]
            self.mom2 = self.resultstr.split("_")[5]
            self.mom3 = self.resultstr.split("_")[6]
            self.mom4 = self.resultstr.split("_")[7]


    def texresultstr(self, num=2):
        tex = ''
        
        if self.flav1 == "pion":
            tex += "\pi \left( "
        elif self.flav1 == "kaon":
            tex += "K \left( "
        elif self.flav1 == "eta":
            tex += "\eta \left( "
        elif self.flav1 == "nucleon":
            tex += "N \left( "
        else:
            print("can't find flav1")
            sys.exit()

        for p in self.mom1:
            tex = tex + p + ","

        tex = tex[:-1] + " \\right) "
        
        if self.flav2 == "pion":
            tex = tex + "\pi \left( "
        elif self.flav2 == "kaon":
            tex = tex + "K \left( "
        elif self.flav2 == "eta":
            tex = tex + "\eta \left( "
        elif self.flav2 == "nucleon":
            tex = tex + "N \left( "
        else:
            print("can't find flav1")
            sys.exit()

        for p in self.mom2:
            if p != "0":
                tex = tex + "-" + p + ","
            else:
                tex = tex + p + ","
        
        tex = tex[:-1] + " \\right) "

        self.resultstr_tex = tex


    def calcptot(self, num=2):
        ptot = []
        if num == 2:
            for i,junk in enumerate(self.mom1):
                ptot.append(str(int(self.mom1[i]) - int(self.mom2[i])))

            self.ptot = ",".join(ptot)

            psq = 0
            for p in ptot:
                psq += int(p)*int(p)
            
            self.psq = str(psq)

        elif num > 2:
            print("not implemented yet")
            sys.exit()
            
    def __init__(self):
        self.ensemble = ''
        self.resultstr = ''
        self.resultstr_tex = ''
        self.ratio_str = ''
        self.mom1 = ''
        self.mom2 = ''
        self.psq = ''
        self.ptot = ''
        self.flav1 = ''
        self.flav2 = ''
        self.energy = ''
        self.energyerr = ''
        self.energyerr_zeros = ''
        self.energyratio = ''
        self.energyratioerr = ''
        self.energyprint = ''
        self.energyratioprint = ''
        self.sampling = ''
