#!/bin/bash

# Parameters
#SBATCH --error=/home/kz9921/oral_args_metrics/multirun/2025-07-09/10-34-28/.submitit/%j/%j_0_log.err
#SBATCH --gres=gpu:4
#SBATCH --job-name=generate_questions
#SBATCH --mem=8GB
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --open-mode=append
#SBATCH --output=/home/kz9921/oral_args_metrics/multirun/2025-07-09/10-34-28/.submitit/%j/%j_0_log.out
#SBATCH --partition=pli-c
#SBATCH --signal=USR2@120
#SBATCH --time=2400
#SBATCH --wckey=submitit

# setup
export HYDRA_FULL_ERROR=1
module purge
module load anaconda3/2024.6
conda activate vllm_env

# command
export SUBMITIT_EXECUTOR=slurm
srun --unbuffered --output /home/kz9921/oral_args_metrics/multirun/2025-07-09/10-34-28/.submitit/%j/%j_%t_log.out --error /home/kz9921/oral_args_metrics/multirun/2025-07-09/10-34-28/.submitit/%j/%j_%t_log.err /home/kz9921/.conda/envs/vllm_env/bin/python -u -m submitit.core._submit /home/kz9921/oral_args_metrics/multirun/2025-07-09/10-34-28/.submitit/%j
