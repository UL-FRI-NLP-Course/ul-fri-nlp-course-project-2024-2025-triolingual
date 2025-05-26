#!/bin/bash
#SBATCH --job-name=mistral-lora-ft
#SBATCH --output=finetune_%j.out
#SBATCH --error=finetune_%j.err
#SBATCH --time=24:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G

module purge
module load Anaconda3/2023.07-2
module load CUDA/11.8.0

conda activate mistral-lora
source $(conda info --base)/etc/profile.d/conda.sh
# module load python/3.10

python finetune_llm.py