#!/bin/bash

# Submit a bunch of slurm jobs

for i in {81..84}
do
	echo $i
	cd sim_$i
	pwd
	sbatch run.slurm
	cd ..
done
