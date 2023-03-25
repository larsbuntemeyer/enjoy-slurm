#!/bin/sh

#SBATCH --partition=shared
#SBATCH --account=ch0636
#SBATCH --dependency=afterany:1:2:3
#SBATCH --kill-on-invalid-dep=yes


echo "Hello World from $(hostname)"
