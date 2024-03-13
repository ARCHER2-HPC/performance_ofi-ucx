#!/bin/bash

# Slurm job options (job-name, compute nodes, job time)
#SBATCH --job-name=castep-DNA
#SBATCH --time=24:00:0
#SBATCH --nodes=128
#SBATCH --tasks-per-node=8
#SBATCH --cpus-per-task=16
#SBATCH --account=z19
#SBATCH --partition=standard
#SBATCH --qos=standard

module load castep/21.11
module load cpe/21.09
export LD_LIBRARY_PATH=$CRAY_LD_LIBRARY_PATH:$LD_LIBRARY_PATH

module list

nruns=3

# Set the number of OpenMP threads per task.
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}

for irun in $(seq 1 ${nruns})
do
   timestamp=$(date +%s)
   srun --distribution=block:block --hint=nomultithread castep.mpi polyA20-no-wat &> polyA20-no-wat_OFI_${SLURM_JOB_NUM_NODES}nodes_${SLURM_CPUS_PER_TASK}threads_run${irun}_id${SLURM_JOB_ID}_${timestamp}.out
   mv polyA20-no-wat.castep polyA20-no-wat_OFI_${SLURM_JOB_NUM_NODES}nodes_${SLURM_CPUS_PER_TASK}threads_run${irun}_id${SLURM_JOB_ID}_${timestamp}.castep
done
