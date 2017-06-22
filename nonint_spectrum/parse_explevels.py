import os
import sys
from levelutils import *

FLAVOURS = ["K", "KB", "pi", "eta", "N"]
ISOMAP = {0: "isosinglet",
          0.5: "isodoublet",
          1: "isotriplet",
          1.5: "isoquartet",
          2: "isoquintet",
          2.5: "isosextet"}

def readlevels(filename, ensem, psq):
    if not filename.endswith('.txt'):
        print("support only for .txt expected levels files")
        sys.exit()

    with open(filename) as f:
        text = f.readlines()

    text = [x.strip('\n') for x in text]

    filename = filename.split("/")[-1]
    flavtype = filename.split("_")[0]
    isospin = filename.split("_")[1]
    strangeness = filename.split("_")[2]
    if isospin[0] == "2":
        isospin = float(isospin[-1])/2.0
    elif isospin[0] == "I":
        isospin = float(isospin[-1])
    else:
        print("can't determine isospin from filename: " + filename)
        sys.exit()
    if flavtype == "bosonic":
        strangeness = float(strangeness[-1])
    elif flavtype == "fermionic":
        strangeness = -1*float(strangeness[-1])
    else:
        print("couldn't figure if fermion or boson from filename: " + filename)
        sys.exit()


    levels = []
    levels_irrep = []

    for x in text:
        if "Irrep = " in x:     # for each new irrep, get levels
            irrep = x.split("Irrep = ")[-1]
            levels.extend(levels_irrep)
            if 'levels_sep' in locals():
                levels_sep.append(levels_irrep)
            else:
                levels_sep = levels_irrep
            levels_irrep = []

        # determine if line is level based on channel isospin: check for isosinglet, etc.
        if any(x.strip().endswith(y) for y in FLAVOURS):
            temp = explevel()
            temp.irrep = irrep
            temp.tex_irrep()
            temp.Npart = 1
            temp.psq = psq
            temp.isospin = isospin
            temp.strangeness = strangeness
            temp.parts.append((x.split()[-1], psq))
            temp.findfitstrings(ensem)
            levels_irrep.append(temp)

        elif ISOMAP[isospin] in x:
            temp = explevel()
            temp.irrep = irrep
            temp.tex_irrep()
            temp.Npart = x.count("PSQ")
            temp.psq = psq
            temp.isospin = isospin
            temp.strangeness = strangeness
            i = 0
            x = x.split()[-1]   # split off end string
            while i < temp.Npart:
                temp.parts.append((x.split("_")[0], x.split("PSQ")[1].split("_")[0]))
                x = x.split("_", 2)[-1]
                i += 1

            temp.findfitstrings(ensem)
            
            check = True
            # only put level in that contain stable particles and the first 3/4 particle states
            for y in temp.parts:
                if not any(y[0] == i for i in FLAVOURS):
                    check = False

            if temp.Npart > 2:
                if any(temp.Npart == j.Npart for j in levels_irrep):
                    check = False

            if check:
                levels_irrep.append(temp)

    # append final irrep
    levels.extend(levels_irrep)
    levels_sep.append(levels_irrep)

    # return list containing sublist for each irrep
    return levels_sep

# TESTING
if __name__ == "__main__":
    junk = readlevels("/home/ruairi/research/expectedlevels/32_240/mom_000/bosonic_I=0_S=0_levels.txt", "32_860", 0)
