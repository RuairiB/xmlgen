#!/bin/bash

# change all filepaths from ruairi-laptop to emilio :: OLD, write in future such that this isn't needed

# sys.path for generate_* files
for f in $(find /latticeQCD/raid6/ruairi/git/xmlgen/ -name '*.py'); do sed -i 's|/home/ruairi/research/xmlgen/|/home/ruairi/git/xmlgen/|g' $f; done

# working dir/inputdir changes
for f in $(find /latticeQCD/raid6/ruairi/git/xmlgen/ -name '*.py'); do sed -i 's|/home/ruairi/research/freeparticle_energies/|/latticeQCD/raid6/ruairi/freeparticle_energies/|g' $f; done

for f in $(find /latticeQCD/raid6/ruairi/git/xmlgen/ -name '*.py'); do sed -i 's|/home/ruairi/research/correlator_data/clover_s32|/latticeQCD/raid8/laph/clover_s32|g' $f; done

for f in $(find /latticeQCD/raid6/ruairi/git/xmlgen/ -name '*.py'); do sed -i 's|/home/ruairi/research/correlator_data/clover_s24|/latticeQCD/raid7/laph/clover_s24|g' $f; done
