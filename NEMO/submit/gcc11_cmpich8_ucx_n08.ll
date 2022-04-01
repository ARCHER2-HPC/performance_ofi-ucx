#!/bin/bash

#SBATCH --job-name=bm_nemo
#SBATCH -o /dev/null
#SBATCH -e /dev/null
#SBATCH --time=02:00:00
#SBATCH --exclusive
#SBATCH --nodes=8
#SBATCH --ntasks=400
#SBATCH --account=<budget code>
#SBATCH --partition=standard
#SBATCH --qos=standard


# Created by: mkslurm_gcc11.sh -S 16 -s 16 -m 2 -C  384 -c  2 -t 02:00:00 -a <budget code> -j nemo


module -q load cpe/21.09
module -q swap PrgEnv-cray PrgEnv-gnu
module -q load cray-hdf5-parallel
module -q load cray-netcdf-hdf5parallel
module -q load xpmem
module -q load perftools-base

module -q swap craype-network-ofi craype-network-ucx
module -q swap cray-mpich cray-mpich-ucx
module -q load libfabric

export LD_LIBRARY_PATH=${CRAY_LD_LIBRARY_PATH}:${LD_LIBRARY_PATH}


# setup resource-related environment
NNODES=${SLURM_JOB_NUM_NODES}
NCORESPN=`expr ${SLURM_CPUS_ON_NODE} \/ 2`
NCORES=`expr ${NNODES} \* ${NCORESPN}`
export OMP_NUM_THREADS=1


# setup app-related environment
CASE=GYRE_PISCES_CFG
ROOT=/path/to/work
APP_NAME=nemo
APP_VERSION=4.0.6
APP_EXE_NAME=nemo.exe
APP_MPI_LABEL=cmpich8
APP_COMMS_LABEL=ucx
APP_COMPILER_LABEL=gcc11
APP_RUN_ROOT=${ROOT}/tests/${APP_NAME}
APP_RUN_PATH=${APP_RUN_ROOT}/${CASE}/results/${APP_COMPILER_LABEL}/${APP_MPI_LABEL}-${APP_COMMS_LABEL}/n${NNODES}
APP_OUTPUT=${APP_RUN_PATH}/${APP_NAME}.o

# setup app run directory
mkdir -p ${APP_RUN_PATH}
cp ${APP_RUN_ROOT}/${CASE}/input/* ${APP_RUN_PATH}/

# run app
RUN_START=$(date +%s.%N)
echo -e "Launching ${APP_EXE_NAME} in detached mode (${APP_MPI_LABEL}-${APP_COMPILER_LABEL}) ${CASE} over ${NNODES} node(s).\n" > ${APP_OUTPUT}

#
cat > ${APP_RUN_PATH}/myscript_wrapper2.sh << EOFB
#!/bin/ksh
#
set -A map /path/to/xios/2.5/gcc/11/cmpich/8/bin/xios_server.exe /path/to/nemo/4.0.6/gcc11/cmpich8/cfgs/GYRE_PISCES_CFG/BLD/bin/nemo.exe
exec_map=( 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 )
#
exec \${map[\${exec_map[\$SLURM_PROCID]}]} 
##
EOFB
chmod u+x ${APP_RUN_PATH}/myscript_wrapper2.sh
#
srun --mem-bind=local --cpu-bind=v,map_cpu:00,0x10,0x20,0x22,0x24,0x26,0x28,0x2a,0x2c,0x2e,0x30,0x32,0x34,0x36,0x38,0x3a,0x3c,0x3e,0x40,0x42,0x44,0x46,0x48,0x4a,0x4c,0x4e,0x50,0x52,0x54,0x56,0x58,0x5a,0x5c,0x5e,0x60,0x62,0x64,0x66,0x68,0x6a,0x6c,0x6e,0x70,0x72,0x74,0x76,0x78,0x7a,0x7c,0x7e,00,0x10,0x20,0x22,0x24,0x26,0x28,0x2a,0x2c,0x2e,0x30,0x32,0x34,0x36,0x38,0x3a,0x3c,0x3e,0x40,0x42,0x44,0x46,0x48,0x4a,0x4c,0x4e,0x50,0x52,0x54,0x56,0x58,0x5a,0x5c,0x5e,0x60,0x62,0x64,0x66,0x68,0x6a,0x6c,0x6e,0x70,0x72,0x74,0x76,0x78,0x7a,0x7c,0x7e,00,0x10,0x20,0x22,0x24,0x26,0x28,0x2a,0x2c,0x2e,0x30,0x32,0x34,0x36,0x38,0x3a,0x3c,0x3e,0x40,0x42,0x44,0x46,0x48,0x4a,0x4c,0x4e,0x50,0x52,0x54,0x56,0x58,0x5a,0x5c,0x5e,0x60,0x62,0x64,0x66,0x68,0x6a,0x6c,0x6e,0x70,0x72,0x74,0x76,0x78,0x7a,0x7c,0x7e,00,0x10,0x20,0x22,0x24,0x26,0x28,0x2a,0x2c,0x2e,0x30,0x32,0x34,0x36,0x38,0x3a,0x3c,0x3e,0x40,0x42,0x44,0x46,0x48,0x4a,0x4c,0x4e,0x50,0x52,0x54,0x56,0x58,0x5a,0x5c,0x5e,0x60,0x62,0x64,0x66,0x68,0x6a,0x6c,0x6e,0x70,0x72,0x74,0x76,0x78,0x7a,0x7c,0x7e,00,0x10,0x20,0x22,0x24,0x26,0x28,0x2a,0x2c,0x2e,0x30,0x32,0x34,0x36,0x38,0x3a,0x3c,0x3e,0x40,0x42,0x44,0x46,0x48,0x4a,0x4c,0x4e,0x50,0x52,0x54,0x56,0x58,0x5a,0x5c,0x5e,0x60,0x62,0x64,0x66,0x68,0x6a,0x6c,0x6e,0x70,0x72,0x74,0x76,0x78,0x7a,0x7c,0x7e,00,0x10,0x20,0x22,0x24,0x26,0x28,0x2a,0x2c,0x2e,0x30,0x32,0x34,0x36,0x38,0x3a,0x3c,0x3e,0x40,0x42,0x44,0x46,0x48,0x4a,0x4c,0x4e,0x50,0x52,0x54,0x56,0x58,0x5a,0x5c,0x5e,0x60,0x62,0x64,0x66,0x68,0x6a,0x6c,0x6e,0x70,0x72,0x74,0x76,0x78,0x7a,0x7c,0x7e,00,0x10,0x20,0x22,0x24,0x26,0x28,0x2a,0x2c,0x2e,0x30,0x32,0x34,0x36,0x38,0x3a,0x3c,0x3e,0x40,0x42,0x44,0x46,0x48,0x4a,0x4c,0x4e,0x50,0x52,0x54,0x56,0x58,0x5a,0x5c,0x5e,0x60,0x62,0x64,0x66,0x68,0x6a,0x6c,0x6e,0x70,0x72,0x74,0x76,0x78,0x7a,0x7c,0x7e,00,0x10,0x20,0x22,0x24,0x26,0x28,0x2a,0x2c,0x2e,0x30,0x32,0x34,0x36,0x38,0x3a,0x3c,0x3e,0x40,0x42,0x44,0x46,0x48,0x4a,0x4c,0x4e,0x50,0x52,0x54,0x56,0x58,0x5a,0x5c,0x5e,0x60,0x62,0x64,0x66,0x68,0x6a,0x6c,0x6e,0x70,0x72,0x74,0x76,0x78,0x7a,0x7c,0x7e, --chdir=${APP_RUN_PATH} ${APP_RUN_PATH}/myscript_wrapper2.sh &>> ${APP_OUTPUT}

RUN_STOP=$(date +%s.%N)
RUN_TIME=$(echo "${RUN_STOP} - ${RUN_START}" | bc)
echo -e "\nsrun time: ${RUN_TIME}" >> ${APP_OUTPUT}


# tidy up
mkdir ${APP_RUN_PATH}/${SLURM_JOB_ID}
mv ${APP_OUTPUT} ${APP_RUN_PATH}/${SLURM_JOB_ID}/
mv ${APP_RUN_PATH}/ocean.output ${APP_RUN_PATH}/${SLURM_JOB_ID}/
mv ${APP_RUN_PATH}/communication_report.txt ${APP_RUN_PATH}/${SLURM_JOB_ID}/
mv ${APP_RUN_PATH}/layout.dat ${APP_RUN_PATH}/${SLURM_JOB_ID}/
mv ${APP_RUN_PATH}/output.namelist.dyn ${APP_RUN_PATH}/${SLURM_JOB_ID}/
mv ${APP_RUN_PATH}/time.step ${APP_RUN_PATH}/${SLURM_JOB_ID}/

rm -f ${APP_RUN_PATH}/*.nc
rm -f ${APP_RUN_PATH}/myscript_wrapper2.sh
