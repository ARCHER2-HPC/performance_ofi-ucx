# NEMO 4.0.6

NEMO is an oceanographic modelling code. Its name is an acronym for Nucleus for European Modelling of the Ocean.
See [https://www.nemo-ocean.eu/](https://www.nemo-ocean.eu/) for further details.


## NEMO Benchmark Information

The ``GYRE_PISCES`` benchmark is an idealized configuration representing a double gyre system in the northern hemisphere.

The term PISCES is an acronym for Pelagic Interaction Scheme for Carbon and Ecosystem Studies.
More about the NEMO ``GYRE_PISCES`` benchmark can be found at [https://forge.ipsl.jussieu.fr/nemo/chrome/site/doc/NEMO/guide/html/cfgs.html#gyre-pisces](https://forge.ipsl.jussieu.fr/nemo/chrome/site/doc/NEMO/guide/html/cfgs.html#gyre-pisces).

Performance is measured as the number of simulation time steps completed per unit of runtime.


## Results

* [Performance analysis script](analysis/NEMO_GYRE_PISCES_perf_analysis.py)
* Calculation:
   - [OpenFabrics](OFI/)
   - [UCX](UCX/)


## Building NEMO 4.0.6 for the ``GYRE_PISCES`` Configuration

First, you need to build XIOS 2.5. Instructions for the Cray, GCC and AMD (AOCC) compilers (CPE 21.09)
can be found at [https://github.com/hpc-uk/build-instructions/tree/main/utils/XIOS](https://github.com/hpc-uk/build-instructions/tree/main/utils/XIOS).

The following instructions show how to set the environment suitable for building NEMO 4.0.6
with either the Cray compiler environment (CCE 12) or the GNU compiler environment (GCC 11)
provided by CPE 21.09.

Setting the environment
-----------------------

```bash
PRFX=/path/to/work/dir

NEMO_LABEL=nemo
NEMO_VERSION=4.0.6
NEMO_ROOT=${PRFX}/${NEMO_LABEL}

XIOS_VERSION=2.5
XIOS_LABEL=xios

module -q load cpe/21.09
module -q load cray-hdf5-parallel
module -q load cray-netcdf-hdf5parallel
module -q load xpmem
module -q load perftools-base

export LD_LIBRARY_PATH=${CRAY_LD_LIBRARY_PATH}:${LD_LIBRARY_PATH}

COMPILER_TAG="cce"
MPI_IMPL_TAG="cmpich"
COMPILER_VER=`echo ${CRAY_CC_VERSION} | cut -d'.' -f1`
MPI_IMPL_VER=`echo ${CRAY_MPICH_PREFIX} | cut -d'/' -f6 | cut -d'.' -f1`

export XIOS_DIR=/path/to/${XIOS_LABEL}/${XIOS_VERSION}/${COMPILER_TAG}/${COMPILER_VER}/${MPI_IMPL_TAG}/${MPI_IMPL_VER}
export LD_LIBRARY_PATH=${XIOS_DIR}/lib:${LD_LIBRARY_PATH}

COMPILER_LABEL=${COMPILER_TAG}${COMPILER_VER}
MPI_IMPL_LABEL=${MPI_IMPL_TAG}${MPI_IMPL_VER}
ARCH_LABEL=X86_archer2-${COMPILER_LABEL}-${MPI_IMPL_LABEL}
BUILD_PATH=${NEMO_ROOT}/${NEMO_VERSION}/${COMPILER_LABEL}/${MPI_IMPL_LABEL}
```

The instructions above need to be amended slightly when building with GCC.
1. Add ``module -q load PrgEnv-gnu`` after the ``cpe/21.09`` module load.
2. Set ``COMPILER_TAG`` to ``"gcc"``.
3. Use ``GNU_VERSION`` instead of ``CRAY_CC_VERSION`` when setting ``COMPILER_VER``.

Notice that for ``PRFX`` and  ``XIOS_DIR`` you should replace ``/path/to`` with something
suitable for your system.

Next, download the NEMO source code and build using your chosen compiler suite for
a specifc NEMO configuration such as ``GYRE_PISCES``.

Downloading the NEMO source
---------------------------

```bash
mkdir -p ${NEMO_ROOT}
cd ${NEMO_ROOT}

svn co https://forge.ipsl.jussieu.fr/${NEMO_LABEL}/svn/${NEMO_LABEL^^}/releases/r${NEMO_VERSION:0:3}/r${NEMO_VERSION} ${BUILD_PATH}

sed -i "s/FC_MODSEARCH => '',/FC_MODSEARCH => '-J',/g" ${BUILD_PATH}/ext/FCM/lib/Fcm/Config.pm
```

Building NEMO for the GYRE_PISCES configuration
-----------------------------------------------

Please ensure that a suitable ``fcm`` has been copied to ``${BUILD_PATH}/arch/``
before commencing the build. Such files suitable for ARCHER2 can be found
at [build/arch-X86_archer2-cce12-cmpich8.fcm](build/arch-X86_archer2-cce12-cmpich8.fcm) and [build/arch-X86_archer2-gcc11-cmpich8.fcm](build/arch-X86_archer2-gcc11-cmpich8.fcm).

```bash
cd ${BUILD_PATH}
  
NEMO_REF=GYRE_PISCES
NEMO_CFG=${NEMO_REF}_CFG
REF_PATH=${BUILD_PATH}/cfgs/${NEMO_REF}
CFG_PATH=${BUILD_PATH}/cfgs/${NEMO_CFG}
EXP00_PATH=${CFG_PATH}/EXP00

rm -rf ${REF_PATH}.sav
cp -r ${REF_PATH} ${REF_PATH}.sav
sed -i 's/key_top/key_nosignedzero/g' ${REF_PATH}/cpp_${NEMO_REF}.fcm

rm -rf ${CFG_PATH}
./makenemo -n ${NEMO_CFG} -r ${NEMO_REF} -m ${ARCH_LABEL} -j 16
rm ${EXP00_PATH}/nemo
```

Setup the ``namelist_cfg`` file for a benchmark run
---------------------------------------------------

```bash
cd ${EXP00_PATH}

sed -i '/using_server/s/false/true/' ${EXP00_PATH}/iodef.xml
sed -i '/ln_bench/s/false/true/' ${EXP00_PATH}/namelist_cfg

sed -i -r -e 's/^( *nn_itend *=).*/\1 1001/' \
    -e 's/^( *nn_write *=).*/\1 2001/' \
    -e 's/^( *nn_stock *=).*/\1 -1/' \
    -e 's/^( *nn_GYRE *=).*/\1 150/' \
    -e 's/^( *rn_rdt *=).*/\1 1200/' \
    ${EXP00_PATH}/namelist_cfg
```

The previous ``sed`` command sets the number of simulation time steps to 1001.
In addition, The ``nn_write`` field is set to a number greater than 1001 in order to 
avoid writing any output files during the simulation. And setting ``nn_stock = -1``
prevents any restart files from being written.

These changes to the settings within ``namelist_cfg`` enable the ``GYRE_PISCES``
benchmark to focus on NEMO compute.


## Running NEMO 4.0.6 with GYRE_PISCES configuration

A number of Slurm submission scripts can be found in the [submit folder](submit/).
This collection covers twelve separate cases, two compiler suites (CCE 12 or GCC 11),
two comms APIs (OFI or UCX) and three node counts (8, 16 or 32).

It is necessary to have a submission script for a specific node count because,
in order to run NEMO efficiently, one must be careful about the placement
of ocean processes (NEMO) and I/O servers (XIOS) across the compute node.

[Previous NEMO performance investigations](https://docs.archer2.ac.uk/research-software/nemo/nemo/#a-performance-investigation) have shown that NEMO runs best if there
are two I/O servers per node, spaced such that each I/O server occupies its
own NUMA region (on ARCHER2, a NUMA region has 16 cores). The ocean
processes are placed across the remaining six NUMA regions such that every
other core is unassigned.

An ARCHER2 compute node has eight NUMA regions and 128 cores.

So, for each node, the first core in the first two NUMA regions are assigned
I/O servers, whereas 48 ocean processes are evenly spaced across the other
six NUMA regions.

The cpu maps laid out in the aforementioned submission scripts cover all
the nodes assigned to the job and hence, the map size increases with node
count.

Each submission script will require editing before you can submit a job.
First, you must replace occurrences of ``<budget code>`` with your actual
budget code, and second, you must replace any occurrence of ``/path/to`` with
a path that makes sense for your setup.

Lastly, the ``GYRE_PISCES`` input data files can be found in the [input folder](input/).
