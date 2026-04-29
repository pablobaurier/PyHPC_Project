#!/bin/sh
#BSUB -q gpuv100
#BSUB -J full_sim
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 02:00
#BSUB -o logs/full_sim_%J.out
#BSUB -e logs/full_sim_%J.err


source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

python src/run_full_simulation.py > results/results1.csv
