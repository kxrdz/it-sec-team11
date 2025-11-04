#!/bin/env bash
cd src

echo "venv von apt installiert "
sudo apt install python3-venv -y > /dev/null 2>&1

echo "Python enveiremnt erstellt mit name pythonenv"
python3 -m venv pythonenv

echo "pythonenv activiert "
source pythonenv/bin/activate

echo "Package installieren "
pip install sympy > /dev/null 2>&1

echo "fertig"
deactivate

