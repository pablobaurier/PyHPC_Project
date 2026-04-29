#!/bin/bash
#BSUB -B 
#BSUB -N 
#BSUB -J task5_miniproject
#BSUB -q hpc 
#BSUB -W 00:20
#BSUB -R "rusage[mem=512MB]"
#BSUB -R "span[hosts=1]"
#BSUB -n 32
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -o task5_miniproject_32.out
#BSUB -e task5_miniproject_32.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

time python project/task5.py 50 32