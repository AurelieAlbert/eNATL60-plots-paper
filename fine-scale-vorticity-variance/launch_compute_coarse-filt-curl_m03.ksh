#!/bin/bash
#SBATCH --nodes=20
#SBATCH --ntasks=480
#SBATCH --constraint=HSW24
#SBATCH -J vortvar
#SBATCH -e vortvar.e%j
#SBATCH -o vortvar.o%j
#SBATCH --time=06:00:00
#SBATCH --exclusive

export PATH=/scratch/cnt0024/hmg2840/albert7a/anaconda3/bin:$PATH
module load openmpi/intel/2.0.1

mpirun -np 480 --interface ib0 python  2020-04-23-AA-fine-scale-vorticity-variance-eNATL60-BLBT02-m03-debug-daskmpi-occigen.py
