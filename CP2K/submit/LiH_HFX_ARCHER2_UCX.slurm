#!/bin/bash

# Slurm job options (name, compute nodes, job time)
#SBATCH --job-name=cp2k_bench
#SBATCH --time=1:30:0
#SBATCH --nodes=512
#SBATCH --tasks-per-node=16
#SBATCH --cpus-per-task=8

#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --account=z19

module load cp2k/cp2k-8.2
export EXE=cp2k.psmp

module load craype-network-ucx
module load cray-mpich-ucx

ldd $(which $EXE)

export OMP_NUM_THREADS=8

NODES=$SLURM_JOB_NUM_NODES
CORES=$((NODES*128))
THREADS=$OMP_NUM_THREADS

export OMP_PLACES=cores

srun --hint=nomultithread --distribution=block:block $EXE -i input_bulk_HFX_3.inp  > HFX_bench-${NODES}nodes-${CORES}cores-${THREADS}threads-${SLURM_JOB_ID}.out

