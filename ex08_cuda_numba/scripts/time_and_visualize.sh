#!/bin/bash
#BSUB -J timing_trials
#BSUB -o logs/timing_trial_%J.out
#BSUB -e logs/timing_trial_%J.err
#BSUB -q hpc
#BSUB -W 00:30
#BSUB -n 1
#BSUB -R "rusage[mem=16GB]"
#BSUB -R "select[model == XeonGold6126]"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python3 src/time_and_visualize.py 1
python3 src/time_and_visualize.py 2
python3 src/time_and_visualize.py 3
python3 src/time_and_visualize.py 4
python3 src/time_and_visualize.py 10
python3 src/time_and_visualize.py 15
python3 src/time_and_visualize.py 20