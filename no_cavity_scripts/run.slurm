#!/bin/bash
#SBATCH --job-name="short"  #  Please attempt to give the job a descriptive name
#SBATCH --partition=gpu
#SBATCH --nodes=1                    # must be 1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1                    # max 4.5 times the number of tasks per node
#SBATCH --mem=16G
#SBATCH --time=8:00:00
#SBATCH --export=ALL



slurm_info_out(){
echo "=================================== SLURM JOB ==================================="
date
echo "The job will be started on the following node(s):"
echo $SLURM_JOB_NODELIST
echo
echo "Number of nodes:    $SLURM_JOB_NUM_NODES"
echo "Number of tasks:    $SLURM_NTASKS"
echo "=================================== SLURM JOB ==================================="
echo "--- SLURM job-script output ---"
}

slurm_startjob () {
slurm_info_out


# Load Terachem Burrata
#export PATH="/data/cmyers7/terachem_2023:$PATH"

# Python and CUDA stuff
#module purge
#module load anaconda3
#CUDA=$(module -t spider cuda 2>/dev/null | grep -Eo 'cuda/[0-9.]+' | sort -V | tail -1 || true)
#if [[ -n $CUDA ]]; then
#  echo "Loading $CUDA"
#  module load "$CUDA"
#else
#  echo "No standalone CUDA module; relying on Anaconda’s cudatoolkit."
#fi


# Load Terachem module load cuda/11.4.0
#module load anaconda3 >> env.out
source ~/.bashrc >> env.out 
conda activate pysces  >> env.out

module load cuda/12.3.0
export TeraChem=/home/cmyers7/code/terachem/build
export PATH=$TeraChem/bin:$PATH
export PATH=/home/cmyers7/code/terachem/build/bin/:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/cmyers7/code/terachem/build/lib/
export TeraChem=/home/cmyers7/code/terachem/build
ldd /home/cmyers7/code/terachem/build/bin/terachem >> env.out
which terachem >>  env.out
#echo $(pwd) >> path.out
path_job=$(pwd)
cd /home/souravmajumdar/scratch/server_list
mkdir server_servernumber
cd server_servernumber
PORT=$((12000 + RANDOM % 1000))
terachem -s $PORT &
path_server=$(pwd)
j=$(hostname -i)

cd $path_job
echo "path server" >> path.out
echo $path_server >> path.out
echo "path_job" >> path.out
echo $path_job >> path.out
sed -i "s/ipserver/$j/g" input_simulation_local.py
sed -i "s|pathserver|$path_server|g" input_simulation_local.py
sed -i "s/portnumber/$PORT/g" input_simulation_local.py
sleep 5

pysces 


echo Job Done
}

slurm_startjob
`
