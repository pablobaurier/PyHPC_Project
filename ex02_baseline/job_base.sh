#!/bin/bash
#BSUB -J project
#BSUB -q hpc
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=512MB]"
#BSUB -R "select[model ==  XeonGold6226R]"
#BSUB -W 1:00
#BSUB -B
#BSUB -N
#BSUB -o out/project_%J.out
#BSUB -e err/project_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026
time python simulate.py 50