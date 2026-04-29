#!/bin/bash
#BSUB -J timing_ref
#BSUB -o logs/jacobi%J.out
#BSUB -e logs/jacobi%J.err
#BSUB -q hpc
#BSUB -W 00:30
#BSUB -n 1
#BSUB -R "rusage[mem=16GB]"
#BSUB -R "select[model == XeonGold6126]"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

# -l flag means line-by-line, -v means view results immediately
kernprof -l -v src/time_and_visualize.py