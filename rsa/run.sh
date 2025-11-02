#!/bin/bash
# run.sh - Startet den ETP Server

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Starte RSA ETP Server..."

# Python-Interpreter ausführen
python3 "$SCRIPT_DIR/src/etp_server.py"
