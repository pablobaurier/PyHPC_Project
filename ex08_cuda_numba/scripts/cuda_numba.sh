#!/bin/sh
#BSUB -q gpuv100
#BSUB -J cuda_numba_test_50
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 00:30
#BSUB -o logs/cuda_numba_test_50_%J.out
#BSUB -e logs/cuda_numba_test_50_%J.err


source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

python src/simulate_cuda_numba.py 4571