## Benchmarking MPI Collective Communication with ReproMPI: OFI and UCX Methodologies

This document details the methodology for benchmarking MPI collective
communication using the ReproMPI benchmark suite, configured for both the
OpenFabrics Interface (OFI) and UCX frameworks on ARCHER2.

### 1\. ReproMPI Benchmarking

ReproMPI is a benchmark suite designed for reproducible measurement of MPI
collective operations. It provides a robust framework for evaluating the
performance of various MPI collective calls across different message sizes and
repetition counts.

#### 1.1. Prerequisites

To build and run ReproMPI, the following software components are required:

  * **MPI library:** A standard MPI implementation (e.g., Cray MPICH).
  * **CMake (version >= 3.22):** A cross-platform build system. For detailed
    instructions on building CMake, refer to this guide: [Downloading,
    Compiling, and Installing CMake on
    Linux](https://geeksww.com/tutorials/operating_systems/linux/installation/downloading_compiling_and_installing_cmake_on_linux.php).
  * **GSL library:** The GNU Scientific Library, which provides a wide range of
    mathematical routines.

#### 1.2. Building ReproMPI

The build process for ReproMPI is consistent regardless of whether OFI or UCX
will be used for execution. The specific network-related modules are loaded
during the run phase, not the build phase.

1.  Clone the ReproMPI repository from its official GitHub source:
    ```bash
    git clone https://github.com/hunsa/reprompi
    ```
2.  Navigate into the newly cloned `reprompi` directory:
    ```bash
    cd reprompi
    ```
3.  Configure the build with CMake. The `-DOPTION_ENABLE_PGCHECKER=ON` flag
    enables additional checks.
    ```bash
    cmake -DOPTION_ENABLE_PGCHECKER=ON .
    ```
4.  Compile the source code using `make`:
    ```bash
    make
    ```
5.  Generate the configuration files, which are essential for ReproMPI's
    execution:
    ```bash
    make config
    ```

#### 1.3. Running ReproMPI on ARCHER2

The critical distinction between OFI and UCX execution lies in the specific
network communication module loaded before launching the MPI processes.

##### 1.3.1. ReproMPI with OpenFabrics Interface (OFI)

To execute ReproMPI utilizing the OFI communication stack, ensure the
appropriate GSL, OFI network, and Cray MPICH modules are loaded, and the `PATH`
environment variable is correctly configured to include the GSL binaries.

```bash
module load gsl
module load craype-network-ofi
module load cray-mpich
export PATH="/work/y07/shared/libs/core/gsl/2.7/CRAYCLANG/10.0/bin:$PATH"
```

An example Slurm job script for running ReproMPI with OFI is provided below:

```bash
#!/bin/bash

# Slurm job options
#SBATCH --job-name=OFI-ReproMPI
#SBATCH --time=2:0:0
#SBATCH --nodes=512                   # Number of compute nodes requested
#SBATCH --ntasks-per-node=128         # Number of MPI tasks to run on each node
#SBATCH --account=[account]           # Replace with your specific project budget code
#SBATCH --partition=standard
#SBATCH --qos=lowpriority
#SBATCH --exclusive
#SBATCH --output=output/MPI_Allgather/512-%x.%j.out

# Load necessary modules and set environment variables
module load PrgEnv-gnu               # Load GNU Programming Environment
module load gsl
module load craype-network-ofi
module load cray-mpich
export PATH="/work/y07/shared/libs/core/gsl/2.7/CRAYCLANG/10.0/bin:$PATH"
module remove darshan                # Remove Darshan module if loaded

method="MPI_Allgather" # Define the MPI collective method to benchmark

echo "=================================================================="
echo "#Lib:OFI"
echo "method=$method"

# Loop for 5 iterations of the benchmark run
for i in {1..5}
do
    echo "#Iteration=$i"

    # Execute the ReproMPI benchmark
    # --calls-list: specifies the MPI collective operation (from $method variable)
    # --msizes-list: defines the message sizes in bytes to test
    # --nrep: sets the number of repetitions for each message size within a single benchmark run
    # --summary=median,mean: requests median and mean statistics in the output
    srun --hint=nomultithread --distribution=block:block ./bin/mpibenchmark --calls-list=$method --msizes-list=1,10,100,1000,10000 --nrep=5 --summary=median,mean

    echo "=================================================================="
done
```
This script configures a Slurm job to execute ReproMPI, specifically targeting
the `MPI_Allgather` collective communication operation. It tests message sizes
ranging from 1 byte to 10,000 bytes.

##### 1.3.2. ReproMPI with Unified Communication X (UCX)

To execute ReproMPI utilizing the UCX communication stack, ensure the
appropriate GSL, UCX network, and Cray MPICH modules are loaded, and the `PATH`
environment variable is correctly configured to include the GSL binaries.

```bash
module load gsl
module load craype-network-ucx
module load cray-mpich-ucx
export PATH="/work/y07/shared/libs/core/gsl/2.7/CRAYCLANG/10.0/bin:$PATH"
```

An example Slurm job script for running ReproMPI with UCX is provided below:

```bash
#!/bin/bash

# Slurm job options
#SBATCH --job-name=UCX-ReproMPI
#SBATCH --time=2:0:0
#SBATCH --nodes=512                   # Number of compute nodes requested - Increased to 512
#SBATCH --ntasks-per-node=128         # Number of MPI tasks to run on each node
#SBATCH --account=[account]]          # Replace with your specific project budget code
#SBATCH --partition=standard
#SBATCH --qos=lowpriority
#SBATCH --exclusive
#SBATCH --output=output/MPI_Allgather/512-%x.%j.out # Redirect job output to a specific file

# Load necessary modules and set environment variables
module load gsl
module load craype-network-ucx
module load cray-mpich-ucx
export PATH="/work/y07/shared/libs/core/gsl/2.7/CRAYCLANG/10.0/bin:$PATH"
module remove darshan                # Remove Darshan module if loaded

method="MPI_Allgather" # Define the MPI collective method to benchmark

echo "=================================================================="
echo "#Lib:UCX"
echo "method=$method"

# Loop for 5 iterations of the benchmark run
for i in {1..5}
do
    echo "#Iteration=$i"

    # Execute the ReproMPI benchmark
    # --calls-list: specifies the MPI collective operation (from $method variable)
    # --msizes-list: defines the message sizes in bytes to test
    # --nrep: sets the number of repetitions for each message size within a single benchmark run
    # --summary=median,mean: requests median and mean statistics in the output
    srun --hint=nomultithread --distribution=block:block ./bin/mpibenchmark --calls-list=$method --msizes-list=1,10,1000,10000 --nrep=5 --summary=median,mean

    echo "=================================================================="
done
```

This script is structurally identical to the OFI version, but it explicitly
loads the UCX-specific network modules (`craype-network-ucx`, `cray-mpich-ucx`)
to ensure that ReproMPI leverages the UCX communication framework for its
benchmarks. The `MPI_Alltoall` collective operation is benchmarked with the same
parameters for consistency.

#### 1.4. Performance Analysis Script (`analyse.py`)

This script analyzes MPI collective communication benchmark data for OFI and UCX
libraries, generating aggregated CSV reports and comparative performance plots
(log-scale and linear-scale) across various MPI methods, node counts, and
message sizes.