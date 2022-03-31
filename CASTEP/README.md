# CASTEP

## CASTEP Benchmark Information

GROMACS DNA benchmark, available from the [CASTEP website](http://www.castep.org/CASTEP/DNA).

Performance is measured by the timing for 10 SCF loops to complete as given in the `polyA20-no-wat.castep` output file.

## Results

* [Performance analysis script](analysis/CASTEP_DNA_perf_analysis.py)
* Calculation:
   - [OpenFabrics](OFI/)
   - [UCX](UCX/)

## Compiling CASTEP 21.11

These instructions are for compiling CASTEP 21.11 on [ARCHER2](https://www.archer2.ac.uk)
using the Cray CCE compilers with OpenMP threading and Cray FFTW and LibSci.

### Extract the source code and prepare the environment.

Unpack the source

```bash
tar -xvf castep-21.11.tar.gz
```

Then load the Cray FFTW module and set up the CPE 21.09 environment:

```bash
module load cpe/21.09
module load cray-fftw
export LD_LIBRARY_PATH=$CRAY_LD_LIBRARY_PATH:$LD_LIBRARY_PATH
```

If you wish to profile with CrayPat-lite, you will need to perform load the following modules instead:

```bash
module load cpe/21.09
module load cray-fftw
module load perftools-base
module load perftools-lite
export LD_LIBRARY_PATH=$CRAY_LD_LIBRARY_PATH:$LD_LIBRARY_PATH
```

### Build and install

As we are using the Cray FFTW and LibSci libraries, we will not need to modify the Makefile or arch file. To build CASTEP, run the commands below. When prompted for the locations of the LAPACK, BLAS and FFTW libraries, you can press 'Enter' without entering anything, as the `cc` compiler wrapper will link these in by itself.

```bash
unset CPU
CC=cc CASTEP_ARCH=linux_x86_64_cray-XT make -j 8 clean
CC=cc CASTEP_ARCH=linux_x86_64_cray-XT make -j 8
```

Once the build is complete, you may install CASTEP in the location of your choice by running:

```bash
make -j 8 INSTALL_DIR=/path/to/install/location/bin install
```

When complete, you will find the `castep.mpi` executable (among others) in your install location's `bin` directory.
