#!/bin/bash

# Script to set up no_cavity sim traj directories

for i in {81..90}
do
	echo $i
	mkdir sim_$i
	cd sim_$i
	pwd
	cp ../input_simulation_local.py .
	cp ../run.slurm .
	# generate a random 5-digit number
        num=$(printf "%05d" $((RANDOM % 1000000)))

	# add random seed to input simulation file 
        sed -i "s/seednumber/$num/g" input_simulation_local.py
        sed -i "s|servernumber|$i|g" run.slurm	
	cd ..
done 
