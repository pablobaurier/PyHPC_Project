#!/bin/bash
#BSUB -B 
#BSUB -N 
#BSUB -J task6_miniproject
#BSUB -q hpc 
#BSUB -W 00:20
#BSUB -R "rusage[mem=512MB]"
#BSUB -R "span[hosts=1]"
#BSUB -n 2
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -o task6_miniproject_2.out
#BSUB -e task6_miniproject_2.err
time python project/task6.py 50 32