# OSU MPI Benchmarks

## Benchmark Information

Ohio State University MPI microbenchmarks. For this case we run the following collective benchmarks:

* Allreduce
* Allgather
* Allgatherv
* Alltoall
* Alltoallv

## Results

* Performance analysis scripts:
   - [Allreduce](analysis/OSU_Allreduce_compare.py)
* Results:
   - [OpenFabrics](OFI/)
   - [UCX](UCX/)

## Compiling OSU microbenchmarks

Setup correct modules:

```bash
module restore
module load PrgEnv-cray
module load cpe/21.09
export LD_LIBRARY_PATH=$CRAY_LD_LIBRARY_PATH:$LD_LIBRARY_PATH
```

The loaded module list when these instructions were written was:

```bash
Currently Loaded Modules:
  1) craype-x86-rome         5) epcc-setup-env      9) cray-dsmml/0.2.1       13) cpe/21.09
  2) libfabric/1.11.0.4.71   6) load-epcc-module   10) cray-libsci/21.08.1.2
  3) craype-network-ofi      7) PrgEnv-cray/8.1.0  11) cray-mpich/8.1.9
  4) bolt/0.7                8) cce/12.0.3         12) craype/2.7.10
```

Download and unpack the microbenchmarks:

```bash
wget https://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-5.9.tar.gz
tar -xvf osu-micro-benchmarks-5.9.tar.gz
cd osu-micro-benchmarks-5.9
```

Compile the microbenchmarks

```bash
./configure CC=cc CXX=CC
make 
make install
```

