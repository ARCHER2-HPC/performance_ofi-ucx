# CP2K

A full description of the CP2K benchmark is provided below.

# CP2K Benchmark Information

We use the LiH-HFX benchmark. According to the [CP2K benchmarks](https://www.cp2k.org/performance) page:

"This is a single-point energy calculation using Quickstep GAPW (Gaussian and Augmented Plane-Waves) with hybrid Hartree-Fock exchange. It consists of a 216 atom Lithium Hydride crystal with 432 electrons in a 12.3 Å3 cell. These types of calculations are generally around one hundred times the computational cost of a standard local DFT calculation, although this can be reduced using the Auxiliary Density Matrix Method (ADMM). Using OpenMP is of particular benefit here as the HFX implementation requires a large amount of memory to store partial integrals. By using several threads, fewer MPI processes share the available memory on the node and thus enough memory is available to avoid recomputing any integrals on-the-fly, improving performance. "

_This benchmark is best for large core/node counts (>24 nodes) as it requires a lot of memory. Using fewer than this number of nodes results in an out of memory error._

## Required files
The input and data files required for this benchmark can be found in the [input](input/) directory in the ARCHER benchmarks repository.

* [CP2K LiH HFX input files](https://github.com/hpc-uk/archer-benchmarks/tree/main/apps/CP2K/LiH_HFX/input)

The submit scripts can be found in the job_scripts directory:

* [Run scripts for CP2K](submit/)

## Results

* [Performance analysis script](analysis/CP2K_LiH-HFX_perf_analysis.py)
* Calculation:
   - [OpenFabrics](OFI/)
   - [UCX](UCX/)

## Running the benchmark

### Setup Calculation

In order to run the benchmark, first a setup calculation must be performed to produce an input wave function file. This setup calculation can be carried out on 2 nodes, taking under a minute.

To run this setup calculation, copy `input_bulk_B88_3.inp` and `BASIS_OPT` into a working directory. Also copy the batch script `setup_ARCHER.pbs` into this working directory, remembering to change the budget code, and path to the `CP2K.psmp` executable. Now submit this job.

Once the job has completed, rename `LiH_bulk_3-RESTART.wfn` to `B88.wfn`. This is the input file required by the benchmark.

### Benchmark Calculation

Once the input file `B88.wfn` has been created (see above), the main benchmark calculation can be run. Copy `input_bulk_HFX_3.inp`, `BASIS_OPT` and `B88.wfn` into a working directory.

Also copy the `LiH_HFX_ARCHER2.pbs` batch script into your work directory, remembering to change the budget code, path to the `CP2K.psmp` executable, as well as the node/core/thread counts to the appropriate values. __Please note:__ the benchmark requires a lot of memory, so must be run on 128 or more nodes. Also, using several OpenMP threads per MPI process is beneficial for saving memory.

Once the benchmark has completed (typically takes <10 minutes) the time taken can be determined from the job's output by looking for `CP2K` in the timing information:

```
-------------------------------------------------------------------------------
 -                                                                             -
 -                                T I M I N G                                  -
 -                                                                             -
 -------------------------------------------------------------------------------
 SUBROUTINE                       CALLS  ASD         SELF TIME        TOTAL TIME
                                MAXIMUM       AVERAGE  MAXIMUM  AVERAGE  MAXIMUM
 CP2K                                 1  1.0    0.178    0.295  200.814  200.816
 qs_energies                          1  2.0    0.000    0.000  200.091  200.093
 scf_env_do_scf                       1  3.0    0.000    0.000  198.017  198.018
 qs_ks_update_qs_env                  8  5.0    0.000    0.000  161.422  161.440
 rebuild_ks_matrix                    7  6.0    0.000    0.000  161.419  161.437
 qs_ks_build_kohn_sham_matrix         7  7.0    0.001    0.001  161.419  161.437
 hfx_ks_matrix                        7  8.0    0.000    0.000  154.464  154.495
```
Or by using `grep`, e.g.

```
$ grep "CP2K      " CP2K_256.o5608893
 CP2K                                 1  1.0    0.178    0.295  200.814  200.816
```


### Compiling CP2K


Further information on CP2K can be found at
[the CP2Kwebsite](https://www.cp2k.org) and on the ARCHER
[CP2K documentation page](http://www.archer.ac.uk/documentation/software/cp2k/).

The official build instructions for CP2K are at
https://www.cp2k.org/howto:compile which recommends that the easiest
way to install prerequisites is via te toolchain script.

For historical reasons, the ARCHER2 build instructions will use the "manual"
route which builds each relevant prerequisite independently.

## General

* We will use the GNU programming environment
* We will only consider the psmp builds for CP2K.
* The autotuned version of libgrid was not built as there were some
  residual problems with the automatic code generation on ARCHER2.

## Dependencies

Following https://www.cp2k.org/howto:compile we have the following
depencencies

CP2K | Name         | Optional | Build?    | Comment
---- | ----         | -------- | ------    | -------
2a.  | Gnu make     | No       | Available |
2b.  | Python       | No       | Available | `module load cray-python`
2c.  | Fortran/C/C++| No       | Available | via module `gcc/9.3.0`
2d.  | BLAS/LAPACK  | No       | Available | via module `cray-libsci/21.04`
2e.  | MPI          | Yes      | Available | via module `cray-mpich/8.1.4`
2f.  | FFTW         | Yes      | Avaialble | `module load cray-fftw`
2g.  | libint       | Yes      | Build     | 
2h.  | libsmm       | Yes      | No        | Using libxsmm
2i.  | libxsmm      | Yes      | Build     |
2j.  | CUDA         | Yes      | --        | Not relevant
2k.  | libxc        | Yes      | Build     |
2l.  | ELPA         | Yes      | Build     |
2m.  | PEXSI        | Yes      | No        | Not required
2n.  | QUIP         | Yes      | No        | Not required
2o.  | PLUMED       | Yes      | No        | Not required
2p.  | spglib       | Yes      | No        | Not required
2q.  | SIRIUS       | Yes      | No        | Not required
2r.  | FPGA         | Yes      | --        | Not relevant


# Preliminaries

## Set GNU programming environment

First of all, we need to switch to the GNU compiler suite and swap to
gcc/9.3.0

```
module restore
module load PrgEnv-gnu
module load cray-fftw
module load cray-python
module load cpe/21.09
module load gcc/9.3.0
export LD_LIBRARY_PATH=$CRAY_LD_LIBRARY_PATH:$LD_LIBRARY_PATH
```

Note that we use gcc 9.3.0 as currently the libint build fails with GCC 11.x.

The full set of loaded modules at compile time:

```
Currently Loaded Modules:
  1) cpe/21.09            5) libfabric/1.11.0.4.71   9) bolt/0.7          13) cray-python/3.9.4.1
  2) cray-fftw/3.3.8.11   6) craype-network-ofi     10) epcc-setup-env    14) gcc/9.3.0
  3) craype/2.7.10        7) cray-dsmml/0.2.1       11) load-epcc-module  15) cray-mpich/8.1.9
  4) craype-x86-rome      8) cray-libsci/21.08.1.2  12) PrgEnv-gnu/8.1.0
```

### Set `CP2K_ROOT`

From the CP2K web site, download the appropriate release of the code: 

```
$ wget https://github.com/cp2k/cp2k/releases/download/v8.2.0/cp2k-8.2.tar.bz2
```
Note: here we get the `.bz2` bundle as it contains the DBCSR submodule
(the `.tar.gz` does not for some reason).

 Untar this into a location on the `/work` file system:
 ```
 $ bunzip2 cp2k-8.2.tar.bz2
 $ tar xvf cp2k-8.2.tar
 $ cd cp2k-8.2
 $ ls
 COPYRIGHT   LICENSE   README.md  arch        data  src    tools
 INSTALL.md  Makefile  REVISION   benchmarks  exts  tests
 $ export CP2K_ROOT=$PWD
```
Note we have set the environment variable `CP2K_ROOT` to be the top-level
CP2K directory. We will refer to this in what follows.

# Build dependencies

The following may be downloaded to a location of choice, but they will all be installed
in `${CP2K_ROOT}/libs`.

## libint

CP2K releases versions of `libint` appropirate for CP2K at https://github.com/cp2k/libint-cp2k
so a download can be selected. A choice is required on the highest `lmax` supported: we choose
`lmax = 4` to limit the size of the static executable.

```
$ wget https://github.com/cp2k/libint-cp2k/releases/download/v2.6.0/libint-v2.6.0-cp2k-lmax-4.tgz
$ tar zxvf libint-v2.6.0-cp2k-lmax-4.tgz
$ cd libint-v2.6.0-cp2k-lmax-4
```

The `libint` web site suggests that `cmake` should be the standard build approach,
but here we use standard `make`.

```
$ CC=cc CXX=CC FC=ftn LDFLAGS=-dynamic ./configure \
                                  --enable-fortran --with-cxx-optflags=-O \
                                  --prefix=${CP2K_ROOT}/libs/libint
$ make
$ make install
```

## libxsmm

From https://github.com/hfp/libxsmm/ download version 1.16.1:

```
$ wget https://github.com/hfp/libxsmm/archive/1.16.1.tar.gz
$ tar zxvf 1.16.1.tar.gz
$ cd libxsmm-1.16.1
```

Compile and install:

```
$  make CC=cc CXX=CC FC=ftn INTRINSICS=1 PREFIX=${CP2K_ROOT}/libs/libxsmm install
```

## libxc

From https://www.tddft.org/programs/libxc/ download version 5.1.4,

```
$ wget -O libxc-5.1.4.tar.gz https://www.tddft.org/programs/libxc/down.php?file=5.1.4/libxc-5.1.4.tar.gz
$ tar zxvf libxc-5.1.4.tar.gz
$ cd libxc-5.1.4
```

Compile and install

```
$ CC=cc CXX=CC FC=ftn ./configure --prefix=${CP2K_ROOT}/libs/libxc
$ make
$ make install
```

## ELPA

From https://elpa.mpcdf.mpg.de/software download e.g.,

```
$ wget https://elpa.mpcdf.mpg.de/html/Releases/2020.05.001/elpa-2020.05.001.tar.gz
$ tar xvf elpa-2020.05.001.tar.gz
$ cd elpa-2020.05.001
```

ELPA install instructions are at https://gitlab.mpcdf.mpg.de/elpa/elpa/blob/master/INSTALL.md

```
$ mkdir build-openmp
$ cd build-openmp
$ CC=cc CXX=CC FC=ftn LDFLAGS=-dynamic ../configure       \
  --enable-openmp=yes --enable-shared=no \
  --disable-avx512        \
  --prefix=${CP2K_ROOT}/libs/elpa-openmp
$ make
$ make install
```

# Compile CP2K itself

## CP2K psmp

The arch file is `$CP2K_ROOT/arch/ARCHER2.psmp` with the contents:

```
CC       = cc -fopenmp
FC       = ftn -fopenmp
LD       = ftn -fopenmp
AR       = ar -r

DATA_DIR   = /work/y07/shared/cp2k/cp2k-8.2/data
CP2K_ROOT  = /work/y07/shared/cp2k/cp2k-8.2

FFTW_INC = /opt/cray/pe/fftw/3.3.8.9/x86_rome/include
FFTW_LIB = /opt/cray/pe/fftw/3.3.8.9/x86_rome/lib

# Options

DFLAGS   = -D__FFTW3 -D__LIBXC  \
           -D__ELPA=202005 -D__LIBINT \
           -D__parallel -D__SCALAPACK -D__MPI_VERSION=3


CFLAGS   = -O3 -mtune=native -funroll-loops -ftree-vectorize 

FCFLAGS  = $(DFLAGS) $(CFLAGS) \
           -I$(CP2K_ROOT)/libs/libint/include  \
           -I$(CP2K_ROOT)/libs/libxc/include  \
           -I$(CP2K_ROOT)/libs/elpa-openmp/include/elpa_openmp-2020.05.001/modules \
           -I$(CP2K_ROOT)/libs/elpa-openmp/include/elpa_openmp-2020.05.001/elpa \
           -I$(FFTW_INC) -ffree-form -std=f2008 -ffree-line-length-none

LDFLAGS  = $(FCFLAGS)  

LIBS     = -L$(CP2K_ROOT)/libs/libint/lib -lint2  \
           -L$(CP2K_ROOT)/libs/libxc/lib -lxcf90 -lxcf03 -lxc \
           -L$(CP2K_ROOT)/libs/elpa-openmp/lib -lelpa_openmp \
           $(PLUMED_DEPENDENCIES) -lz \
           -L$(FFTW_LIB) -lfftw3 -lfftw3_threads \
           -ldl -lstdc++ -lpthread

```

Finally, compile CP2K:

```
$ cd ${CP2K_ROOT}
$ make ARCH=ARCHER2 VERSION=psmp
```

