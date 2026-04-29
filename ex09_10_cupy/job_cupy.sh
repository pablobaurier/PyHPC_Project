#!/bin/bash
#BSUB -J cupy_nsys
#BSUB -q c02613
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 10
#BSUB -B
#BSUB -N
#BSUB -o out/cupy_%J.out
#BSUB -e err/cupy_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

time python simulate.py 50
#nsys profile -o cupy_report python simulate.py 50