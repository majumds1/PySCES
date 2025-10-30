#!/bin/bash

# script for submitting a bunch of slurm jobs

for i in {81..90}
do
	echo $i
	cd sim_$i
	pwd
	sbatch run.slurm
	cd ..
	sleep 3
done
