#!/bin/sh 

#BSUB -q hpc
#BSUB -J ex07_g101
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -W 00:10
#BSUB -N 
#BSUB -o out/Output_%J.out 
#BSUB -e err/Output_%J.err 


# Initialize Python environment 
source /dtu/projects/02613_2025/conda/conda_init.sh 
conda activate 02613_2026


# Run Python script 
# python simulate_PB.py 50

python simulate_PB_2.py 50



