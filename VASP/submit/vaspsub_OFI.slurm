#!/bin/bash
#SBATCH --job-name=VASP646464
#SBATCH --nodes=64
#SBATCH --tasks-per-node=64
#SBATCH --cpus-per-task=2
#SBATCH --time=2:0:0
#SBATCH --account=z19
#SBATCH --partition=standard
#SBATCH --qos=standard

module load vasp/6/6.3.0

VASP_EXE=vasp_gam

ncore=64
cpn=64
threads=1
nodes=$SLURM_JOB_NUM_NODES
casename="TiO2MCC"
srunopts="--hint=nomultithread --distribution=block:block"

uuid=$(uuidgen)
rundir=${casename}_${uuid}

mkdir ${rundir}

cp input/KPOINTS ${rundir}/
cp input/POSCAR ${rundir}/
cp input/POTCAR ${rundir}/
cp input/INCAR.base ${rundir}/INCAR
echo "NCORE=${ncore}" >> ${rundir}/INCAR

cd ${rundir}

cores=$(( nodes * cpn ))
timestamp=$(date '+%Y%m%d%H%M')
resfile="${casename}_${nodes}nodes_${cores}cores_${threads}threads_${ncore}NCORE_${timestamp}.OUTCAR"
TMPDIR=$PWD

export OMP_NUM_THREADS=${threads}
rm WAVECAR
srun ${srunopts} $VASP_EXE
sleep 30

mv OUTCAR ../${resfile}

cd ../
rm -r ${rundir}

