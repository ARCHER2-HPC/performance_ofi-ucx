# VASP

## VASP Benchmark Information

DFT TiO2 benchmark. This benchmark was originally sourced from the UK Materials Modelling Hub. Thanks to
them for sharing this benchmark.

The input for the TiO2 benchmark can be found in the
[input subdirectory in the ARCHER Benchmark repository](https://github.com/hpc-uk/archer-benchmarks/tree/main/others/VASP/TiO2/input).
The POTCAR file needs to be constructed from your own VASP installation of the basis
set files. You will need the `Ti` and `O` PAW PBE basis set files concatenated together.

Performance is measured by the timing for `LOOP+` from the OUTCAR file.

## Results

* [Performance analysis script](analysis/VASP_TiO2_perf_analysis.py)
* Calculation:
   - [OpenFabrics](OFI/)
   - [UCX](UCX/)

## Compiling VASP 6.3.0

These instructions are for compiling VASP 6.3.x on [ARCHER2](https://www.archer2.ac.uk)
using the GCC compilers including the use of OpenMP

We assume that you have obtained the VASP source code from the VASP website along
with any relevant patches.

In these build instructions we use HPE Cray LibSci and the HPE Cray provided
FFTW library to provide the numerical performance libraries. You can use the
AMD AOCL versions instead but our experience is that there is little difference
in performance between LibSci/FFTW and AOCL on ARCHER2.

Unpack the VASP source code and apply patches
---------------------------------------------

Unpack the source

```bash
tar -xvf vasp.6.3.0.tar.gz
```

Setup correct modules
---------------------

```bash
module load PrgEnv-gnu
module load cray-fftw
```

The loaded module list when these instructions were written was:

```bash
Currently Loaded Modules:
  1) gcc/10.2.0        4) libfabric/1.11.0.4.71    7) xpmem/2.2.40-7.0.1.0_2.7__g1d7a24d.shasta  10) bolt/0.7          13) PrgEnv-gnu/8.0.0
  2) craype/2.7.6      5) craype-network-ofi       8) cray-mpich/8.1.4                           11) epcc-setup-env
  3) craype-x86-rome   6) perftools-base/21.02.0   9) cray-libsci/21.04.1.1                      12) load-epcc-module 
```

Create makefile.include
-----------------------

The new build process for VASP (introduced from version 5.4.1) requires the
correct options to be set in makefile.include in the root directory of the
source distribution.

The makefile.include used for the GCC compilers on ARCHER2 can be downloaded from:

* [6.3.0_makefile.include.ARCHER2_GCC_omp](https://github.com/hpc-uk/build-instructions/blob/main/apps/VASP/6.3.0_makefile.include.ARCHER2_GCC_omp)

This build uses:

* HPE Cray LibSci for linear algebra
* FFTW 3 for FFT's

You should copy this file to the root directory of the VASP source distribution
and then rename it to "makefile.include":

```bash
cp 6.3.0_makefile.include.ARCHER2_GCC_omp makefile.include
```

Build VASP
----------

You build all the VASP executables with:

```bash
make all
```

This will produce the following executables in the bin directory:

* `vasp_std` - Multiple k-point version
* `vasp_gam` - GAMMA-point version
* `vasp_ncl` - Non-collinear version

All versions include the additional MD algorithms accessed via the MDALGO keyword.
