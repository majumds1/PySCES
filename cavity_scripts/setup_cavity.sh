#!/bin/bash

# Setup directories for cavity trajs

# Read all seeds into an array
mapfile -t seeds < seed.out
j=0
for i in {81..90}
do
	echo $i
	mkdir sim_$i
	cd sim_$i
	pwd
	cp ../input_simulation_local.py .
	cp ../run.slurm .
	# get correct seed associated with no_cavuty traj
	seed=${seeds[$((j))]}
	j=$((j+1))

	# add random seed to input simulation file 
        sed -i "s/seednumber/$seed/g" input_simulation_local.py
        sed -i "s|servernumber|$i|g" run.slurm	
	cd ..
done 
