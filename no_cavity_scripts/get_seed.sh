#!/bin/bash

# Script to extract the random seed from no_cavitys trajs

rm seed.out
for i in {81..90}       # Provide correct trajectory numbers
do
	echo $i
	cd sim_$i
	grep 'input_seed' input_simulation_local.py | awk {'print $3'} >> ../seed.out
	cd ..
done     
