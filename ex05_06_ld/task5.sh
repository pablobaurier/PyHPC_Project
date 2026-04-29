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
time python project/task5.py 50 32