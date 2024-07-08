#!/bin/bash

echo "Starting virtual environment..."


if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created in $(pwd)"
fi


source venv/bin/activate

echo "Virtual environment activated."

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "Dependencies installed."

export PYTHONPATH=$(pwd)

python3 scripts/run_my_project.py


deactivate

echo "Virtual environment deactivated."