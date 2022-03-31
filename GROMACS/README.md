# GROMACS

## GROMACS Benchmark Information

GROMACS benchPEP benchmark.

Performance is measured in the ns/day output given by the GROMACS `.log` files.

## Results

* [Performance analysis script](analysis/GROMACS_benchPEP_perf_analysis.py)
* Calculation:
   - [OpenFabrics](OFI/)
   - [UCX](UCX/)

## Compiling GROMACS 2021.5

These instructions are for compiling GROMACS 2021.5 on [ARCHER2](https://www.archer2.ac.uk)
using the GCC compilers with OpenMP threading.

### Extract the source code and prepare the environment.

Unpack the source

```bash
tar -xvf gromacs-2021.5.tar.gz
```

Then load the modules and set up the CPE 21.09 environment:

```bash
module load cpe/21.09
module swap PrgEnv-cray PrgEnv-gnu
module load cmake/3.21.3
export LD_LIBRARY_PATH=$CRAY_LD_LIBRARY_PATH:$LD_LIBRARY_PATH
```

If you wish to profile with CrayPat-lite, you will need to perform load the following modules instead:

```bash
module load cpe/21.09
module swap PrgEnv-cray PrgEnv-gnu
module load cmake/3.21.3
module load perftools-base
module load perftools-lite
export LD_LIBRARY_PATH=$CRAY_LD_LIBRARY_PATH:$LD_LIBRARY_PATH
```

Finally, set the following environment variables:

```bash
export CC=cc
export CXX=CC
export GROMACS_PREFIX=/path/to/install/location
```

where you should choose `GROMACS_PREFIX` to be the location you want to install the software to.

### Configure, build and install

Move into the new GROMACS source code directory you just extracted, and create a build directory. Then move inside that.

```bash
cd gromacs-2021.5
mkdir build
cd build
```

Configure the CMake build:

```bash
cmake .. -DGMX_MPI=ON -DGMX_OPENMP=ON -DGMX_GPU=OFF -DGMX_X11=OFF -DGMX_DOUBLE=OFF -DGMX_BUILD_OWN_FFTW=ON -DCMAKE_INSTALL_PREFIX=$GROMACS_PREFIX
```

Finally, build GROMACS and then install it to `$GROMACS_PREFIX`.

```bash
make -j 8
make install
```

This will produce the `gmx_mpi` executable in `$GROMACS_PREFIX/bin` to be used for the benchmarks.
