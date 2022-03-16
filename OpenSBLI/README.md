# OpenSBLI

A full description of the OpenSBLI benchmark is provided below.

* [Run scripts for OpenSBLI](submit/)
* [OpenSBLI benchmark source code](https://github.com/ARCHER-CSE/archer-benchmarks/tree/master/apps/OpenSBLI/source)

# OpenSBLI Benchmark Information

Satya P Jammy

Aerodynamics and Flight Mechanics Research group, University of Southampton, U.K

## Overview

The benchmark test case setup using OpenSBLI is the Taylor-Green vortex problem in a cubic domain of length 2pi. The code was setup to compute the validation, strong scaling and weak scaling simulations across architectures.

* [Strong scaling performance analysis script](analysis/OpenSBLI_1024ss_benchmark.py)
* Strong scaling results:
   - [OpenFabrics](OFI/)
   - [UCX](UCX/)

## Input file

For the large size, strong scaling benchmark the input file `input` has the following entries

```
ss 1024 100 0
```

These entries are:

- `ss` - Strong scaling (fixed for all runs)
- `1024` - 1024 cubed size (fixed for all runs)
- `100` - 100 iterations (varies depending on number of nodes used)
- `0` - Do not write HDF5 output (fixed for all runs)

## Compiling on ARCHER2

Versions used:

 - Compiler: CCE (Cray) 12.0.3
 - MPI: Cray MPICH 8.1.4
 - HDF5: 1.12.0.7

Loaded modules at compile time:

```
  1) craype-x86-rome         5) epcc-setup-env      9) cray-dsmml/0.2.1             13) craype/2.7.10
  2) libfabric/1.11.0.4.71   6) load-epcc-module   10) cray-hdf5-parallel/1.12.0.7  14) cpe/21.09
  3) craype-network-ofi      7) PrgEnv-cray/8.1.0  11) cray-libsci/21.08.1.2
  4) bolt/0.7                8) cce/12.0.3         12) cray-mpich/8.1.9
```

### Build OPS

```bash
cd OPS/ops/c
```

Load the required modules:

```bash
module load PrgEnv-cray
module load cray-hdf5-parallel
module load cpe/21.09
```

Set the required environment variables:

```bash
export OPS_COMPILER=cray
export OPS_INSTALL_PATH=/work/t01/t01/user/benchmark/ARCHER/OpenSBLI/OPS/ops
export MPI_INSTALL_PATH=
export HDF5_INSTALL_PATH=
```

As the Cray C/C++ compiler is Clang-based, move the options from the
Clang section of the `Makefile` to the Cray section. The MPI C compiler
should still be `cc` and the MPI C++ compiler `CC`. The Cray section in
`Makefile` should look like:

```
ifeq ($(OPS_COMPILER),cray) # CCE 10, based on Clang
  CC        := cc
  CUDA_ALIGNE_FLAG := -D__x86_64 -D__align__\(n\)=__attribute__\(\(aligned\(n\)\)\) -D__location__\(a\)=__annotate__\(a\) -DCUDARTAPI=
  CCFLAGS   := -O3 -std=c99 -fPIC -DUNIX -Wall -ffloat-store
  CXX       := CC
  CXXFLAGS  := -fPIC -DUNIX -Wall
  MPICXX    := CC
  MPICC     := cc
  MPIFLAGS  := $(CXXFLAGS)
else
```

Build the OPS library:

```bash
make clean
make mpi
```

### Build the OpenSBLI benchmark

Move to the benchmark directory:

```bash
cd ../../../Benchmark
```

As the Cray C/C++ compiler is Clang-based, move the options from the
Clang section of the `Makefile` to the Cray section. The MPI C compiler
should still be `cc` and the MPI C++ compiler `CC`. The Cray section in
`Makefile` should look like:

```
ifeq ($(OPS_COMPILER),cray)
  CPP       = CC
    CUDA_ALIGN_FLAG := -D__x86_64 -D__align__\(n\)=__attribute__\(\(aligned\(n\)\)\) -D__location__\(a\)=__annotate__\(a\) -DCUDARTAPI=
ifdef DEBUG
  CCFLAGS   = -O2
else
  CCFLAGS   = -O3 -fPIC -DUNIX -Wall
endif
  CPPFLAGS  = $(CCFLAGS)
  OMPFLAGS  = -fopenmp
  MPICPP    = CC
  MPICC     = cc
  MPIFLAGS  = $(CPPFLAGS)
else
```

Once this is all setup, you can compile the benchmark with:

```bash
make clean
make OpenSBLI_mpi_openmp
```



