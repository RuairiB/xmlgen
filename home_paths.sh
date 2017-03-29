#!/bin/bash

# change all filepaths from emilio to ruairi-laptop

# sys.path for generate_* files
for f in $(find /home/ruairi/research/xmlgen/ -name '*.py'); do sed -i 's|/home/ruairi/git/xmlgen/|/home/ruairi/research/xmlgen/|g' $f; done

# working dir/inputdir changes
for f in $(find /home/ruairi/git/xmlgen/ -name '*.py'); do sed -i 's|/latticeQCD/raid6/ruairi/freeparticle_energies/|/home/ruairi/research/freeparticle_energies/|g' $f; done

for f in $(find /home/ruairi/git/xmlgen/ -name '*.py'); do sed -i 's|/latticeQCD/raid8/laph/clover_s32|/home/ruairi/research/correlator_data/clover_s32|g' $f; done

for f in $(find /home/ruairi/git/xmlgen/ -name '*.py'); do sed -i 's|/latticeQCD/raid7/laph/clover_s24|/home/ruairi/research/correlator_data/clover_s24|g' $f; done
