#!/bin/bash
messege="$1"
current_directory=$(dirname "$(readlink -f "$0")")
venv_directory="$current_directory/myenv/bin/activate"
module_initiator_directory="$current_directory/main.py"

source $venv_directory
python -V
output=$(python $module_initiator_directory $messege)
echo "Python script output: $output"
