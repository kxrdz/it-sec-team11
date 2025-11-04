#!/usr/bin/env bash
cd "src"
source pythonenv/bin/activate
python3 rsa-schluessel.py
echo "Kompilierung abgeschlossen."

deactivate