#!/bin/bash

#SBATCH --job-name=osu_bench
#SBATCH --time=0:20:0
#SBATCH --nodes=8
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1

#SBATCH --partition=standard
#SBATCH --qos=short
#SBATCH --account=z19

module load PrgEnv-gnu
module load cpe/21.09
module swap craype-network-ofi craype-network-ucx
module swap cray-mpich cray-mpich-ucx
export LD_LIBRARY_PATH=$CRAY_LD_LIBRARY_PATH:$LD_LIBRARY_PATH
export OMP_NUM_THREADS=1

ml

ldd ../osu-micro-benchmarks-5.9/mpi/collective/osu_allreduce

benchmarks="osu_allreduce osu_allgather osu_allgatherv osu_alltoall osu_alltoallv"

# Launch the parallel job
for benchmark in $benchmarks
do
  timestamp=$(date '+%Y%m%d%H%M')
  resfile=${benchmark}_${SLURM_JOB_NUM_NODES}nodes_${SLURM_NTASKS}processes_${timestamp}.dat
  echo "== Nodes = $SLURM_JOB_NUM_NODES" > $resfile
  echo "== Processes = $SLURM_NTASKS" >> $resfile
  srun --hint=nomultithread --distribution=block:block ../osu-micro-benchmarks-5.9/mpi/collective/$benchmark >> ${resfile}
done

