#!/bin/bash
#BSUB -J logs/visualize_floor_plans
#BSUB -o logs/visualize_floor_plans%J.out
#BSUB -e logs/visualize_floor_plans%J.err
#BSUB -q hpc
#BSUB -W 00:20
#BSUB -n 1
#BSUB -R "rusage[mem=16GB]"
#BSUB -R "select[model == XeonGold6126]"

# --- Environment Setup ---
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

# Execute
python3 simulate.py


