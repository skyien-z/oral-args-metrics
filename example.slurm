#!/bin/bash
#SBATCH --job-name=llama70b  # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --mem=8G
#SBATCH --gres=gpu:4
#SBATCH --partition=pli-c
#SBATCH --time=1:59:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends

module purge
module load anaconda3/2024.6
conda activate vllm_env

python generate_questions.py model_path=/scratch/gpfs/kz9921/transformer_cache/Llama-3.3-70B-Instruct
