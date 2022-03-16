#!/bin/bash
#SBATCH --job-name=TGV1024ss
#SBATCH --time=1:0:0
#SBATCH --nodes=1024
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1

#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --account=z19

module load cpe/21.09
module load craype-network-ucx
module load cray-mpich-ucx
export LD_LIBRARY_PATH=$CRAY_LD_LIBRARY_PATH:$LD_LIBRARY_PATH

osblipath="/work/z19/z19/aturner/software/OpenSBLI/Benchmark"

nodes=$SLURM_JOB_NUM_NODES
casename="TGV1024ss"
cpn=128
cores=$(( nodes * cpn ))

cp input.large input

threadlist="1"

for threads in $threadlist
do
   timestamp=$(date '+%Y%m%d%H%M')
   resfile="${casename}_${nodes}nodes_${cores}cores_${threads}threads_${timestamp}.out"
   TMPDIR=$PWD
   export OMP_NUM_THREADS=${threads}
   tpn=$(( cpn / threads ))
   tasks=$(( tpn * nodes ))
   srun --unbuffered --ntasks=$tasks --tasks-per-node=$tpn --cpus-per-task=$threads --hint=nomultithread --distribution=block:block  ${osblipath}/OpenSBLI_mpi_openmp > $resfile
   sleep 120
done

