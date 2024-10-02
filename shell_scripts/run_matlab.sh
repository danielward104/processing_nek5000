#!/bin/bash
#
# Use the cwd
#$ -cwd
# Export variable 
#$ -V
# Request time
#$ -l h_rt=48:00:00
# Request number of processors
# -l np=160
#$ -pe ib 1
# Request memory
#$ -l h_vmem=4G
# Send to maths node.
#$ -P maths
# Send email when starting/finishing
#$ -m be

script_name=plot_evolvingColourmap

matlab -nodisplay -nosplash -nodesktop -r ''"${script_name}"';exit;'

#matlab -nodisplay -nosplash -nodesktop -r 'run('"${script_name}"');exit;'
