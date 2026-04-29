#!/bin/bash
#BSUB -J visualize_input
#BSUB -o logs/visualize_input%J.out
#BSUB -e logs/visualize_input%J.err
#BSUB -q hpc
#BSUB -W 00:10
#BSUB -n 1
#BSUB -R "rusage[mem=8GB]"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python3 src/visualize_input.py  