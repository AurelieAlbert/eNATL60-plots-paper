#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --constraint=HSW24
#SBATCH -J vortvar
#SBATCH -e vortvar.e%j
#SBATCH -o vortvar.o%j
#SBATCH --time=00:06:00
#SBATCH --exclusive

export PATH=/scratch/cnt0024/hmg2840/albert7a/anaconda3/bin:$PATH
module load openmpi/intel/2.0.1

python test-workers-jobqueue.py
