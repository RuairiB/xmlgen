import os
import sys

sys.path.append(os.path.abspath("/home/ruairi/git/xmlgen/logscraper/"))
from logutils import *

# Given set of levels (separated by irrep), pull corresponding energies (& TeX'd particle content?) from logs
# NOTE: for now, logs separate for specific Npart
# This may be slow, need a better way of parsing logs
def pullenergies(levels, log1, log2, log3, log4, ensemble, sampling):
    # perform some checks here

    for irrep in levels:
        for level in irrep:
            if level.Npart == 1:
                searchlog(level, log1, ensemble, sampling)
            elif level.Npart == 2:
                searchlog(level, log2, ensemble, sampling)
            elif level.Npart == 3:
                searchlog(level, log3, ensemble, sampling)
            elif level.Npart == 4:
                searchlog(level, log4, ensemble, sampling)
            else:
                print("wrong Npart (" + str(level.Npart) + ") for level in " + level.irrep + " irrep")
                sys.exit()
    # check here for correct/complete TeX and such, if not, do it?


# search particular set of logs for given particle combination -- add level.energyprint, etc.
def searchlog(level, logs, ensemble, sampling):
    level.sampling = sampling
    logs_pruned = []
    if ensemble == "32_860":
        ensemble = "s32"
    elif ensemble == "24_840":
        ensemble = "s24"
    else:
        print("bad ensemble string")

    for x in logs:
        if ensemble in x.ensemble and x.sampling == sampling:
            logs_pruned.append(x)

    if len(logs_pruned) < 1:
        print("didn't get any levels for " + ensemble + "  " + sampling + " in the irrep: " + level.irrep)

    parts = []
    for part in level.parts:
        if part[0] == "K" or part[0] == "KB":
            parts.append(("kaon", part[1]))
        elif part[0] == "N":
            parts.append(("nucleon", part[1]))
        elif part[0] == "pi":
            parts.append(("pion", part[1]))
        elif part[0] == "eta":
            parts.append(("eta", part[1]))
        else:
            print("need some help figuring out the flavour for " + part[0])
            sys.exit()


    # check = True
    temp = linsuperlog()
    for log in logs_pruned:
        parts_log = [(log.flav1, log.psq1)]
        if len(parts) > 1:
            parts_log.append((log.flav2, log.psq2))
        if len(parts) > 2:
            parts_log.append((log.flav3, log.psq3))
        if len(parts) > 3:
            parts_log.append((log.flav4, log.psq4))
        if len(parts) > 4:
            print("too many particles (" + len(parts) + "), help me")
            sys.exit()

        if sorted(parts) == sorted(parts_log):
            check = True
            temp = log
            break
        else:
            check = False

    if check:
        # assign things
        level.resultstr_tex = temp.resultstr_tex
        level.energyprint = temp.energyprint
        level.energyratioprint = temp.energyratioprint
        level.ensemble = temp.ensemble
        del temp
    # else:
    #     print("couldn't find log for one of the levels")
    #     sys.exit()


def textable_irrep(destination, irrep, ensemble, psq, sampling):
    irrep.sort(key=lambda k: k.energyprint.split("(")[0])
    f = open(destination + ".tex", 'w')

    if ensemble == "32_860":
        ensemble = "clover\\_s32\\_t256\\_ud860\\_s743"
    elif ensemble == "24_840":
        ensemble = "clover\\_s24\\_t128\\_ud840\\_s743"
    else:
        print("What ensemble are you " + ensemble + "?")

    if len(irrep) != 0:
        # print header, environment, hlines, etc
        f.write("\\begin{longtable}{| c || c | c |}\n")
        f.write("\\hline\n")
        f.write("Particle content & $a_t E$ & $\\frac{E}{m_K}$ \\\\\n")
        f.write("\\hline\n")

        threshold = False
        # print out table content
        for x in irrep:
            if x.resultstr_tex != '':
                if x.Npart > 2:
                    threshold = True
                    f.write("$ {\\color{red}" + x.resultstr_tex + "}$ & {\\color{red}" + x.energyprint + "} & {\\color{red}" + x.energyratioprint + "} \\\\ \n")
                elif threshold:
                    f.write("$ {\\color{blue}" + x.resultstr_tex + "}$ & {\\color{blue}" + x.energyprint + "} & {\\color{blue}" + x.energyratioprint + "} \\\\ \n")
                else:
                    f.write("$ " + x.resultstr_tex + "$ & " + x.energyprint + " & " + x.energyratioprint + " \\\\ \n")

        # print bottom hline, end environment, etc
        f.write("\\hline\n")
        f.write("\\captionsetup{justification=centering}\n")
        f.write("\\caption{$I = " + irrep[0].isospin_tex + "$,  $S = " + str(int(irrep[0].strangeness)) + "$,  $P^2 = " + str(psq) + "$: Non-interacting spectrum of stable hadrons in the $" + irrep[0].irrep_tex + "$ irrep, on the \\vb{" + ensemble + "} ensemble with " + sampling + " resampling.}\n")
        f.write("\\end{longtable}\n")
        # f.write("\\clearpage\n")
        f.close()





class explevel:
    def findfitstrings(self, ensem):
        if ensem == "32_860":
            fudge = ["E1_kaon_4_35P0tsgs",
                     "E1_kaon_5_34P1tsgs",
                     "E1_kaon_5_35P2tsgs",
                     "E1_kaon_5_35P3tsgs",
                     "E1_kaon_4_35P4tsgs",
                     "E1_kaon_4_35P5tsgs",
                     "E1_kaon_4_35P6tsgs",
                     "E1_pion_3_35P0tsgs",
                     "E1_pion_4_35P1tsgs",
                     "E1_pion_4_35P2tsgs",
                     "E1_pion_4_35P3tsgs",
                     "E1_pion_4_35P4tsgs",
                     "E1_pion_4_35P5tsgs",
                     "E1_pion_4_35P6tsgs",
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
                     "E1_pion_4_35P5tsgs",
                     "E1_pion_4_35P6tsgs",
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

        fitlist = []
        for x in self.parts:
            if x[0] == "K" or x[0] == "KB":
                flav = "kaon"
            elif x[0] == "N":
                flav = "nucleon"
            else:
                flav = x[0]

            flavs = [s for s in fudge if flav in s]

            psq = "P" + str(x[1])
            fitlist.append(''.join([s for s in flavs if psq in s]))

        self.fitlist = fitlist


    def tex_irrep(self):
        self.irrep_tex = self.irrep
        if "p" in self.irrep:
            self.irrep_tex = self.irrep_tex.replace("p", "^{+}")
        elif "m" in self.irrep:
            self.irrep_tex = self.irrep_tex.replace("m", "^{-}")
        if "u" in self.irrep:
            self.irrep_tex = self.irrep_tex.replace("u", "_{u}")
        elif "g" in self.irrep:
            self.irrep_tex = self.irrep_tex.replace("g", "_{g}")

    def tex_isospin(self):
        if self.isospin == 0.5:
            self.isospin_tex = "\\frac{1}{2}"
        elif self.isospin == 1.5:
            self.isospin_tex = "\\frac{3}{2}"
        elif self.isospin == 2.5:
            self.isospin_tex = "\\frac{5}{2}"
        elif self.isospin == 3.5:
            self.isospin_tex = "\\frac{7}{2}"
        else:
            self.isospin_tex = str(int(self.isospin))

    def __init__(self):
        self.Npart = 0
        self.parts = []         # list of tuples: (flavour, PSQ)
        self.psq = 0
        self.irrep = ''
        self.irrep_tex = ''
        self.isospin = 0
        self.isospin_tex = 0
        self.strangeness = 0
        self.fitlist = ''
        self.resultstr_tex = ''
        self.energyprint = ''
        self.energyratioprint = ''
        self.sampling = ''
        self.ensemble = ''
