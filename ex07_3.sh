#!/bin/sh 

#BSUB -q hpc
#BSUB -J ex07_g101
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -W 01:30
#BSUB -N 
#BSUB -o out/Output_%J.out 
#BSUB -e err/Output_%J.err 


# Initialize Python environment 
source /dtu/projects/02613_2025/conda/conda_init.sh 
conda activate 02613_2026


# Run Python script 
# python simulate_PB.py 50


python simulate_PB_3.py 1
python simulate_PB_3.py 2
python simulate_PB_3.py 3

# python simulate_PB_3.py 10
# python simulate_PB_3.py 20
# python simulate_PB_3.py 30
# python simulate_PB_3.py 40
# python simulate_PB_3.py 50
# python simulate_PB_3.py 60

# # python simulate_PB_3.py 70
# # python simulate_PB_3.py 80
# # python simulate_PB_3.py 90
# # python simulate_PB_3.py 100
# # python simulate_PB_3.py 150
# # python simulate_PB_3.py 200

