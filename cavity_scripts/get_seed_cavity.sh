#!/bin/bash

# script to get cavity input seeds ( should match no-cavity ones)

rm seed_new.out
for i in {81..90}
do
	echo $i
	cd sim_$i
	grep 'input_seed' input_simulation_local.py | awk {'print $3'} >> ../seed_new.out
	cd ..
done     
