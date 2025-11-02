#!/bin/bash
# install.sh - Installiert die Software auf dem Zielhost

if [ -z "$1" ]; then
    echo "Usage: $0 <host-ip>"
    exit 1
fi

HOST_IP=$1
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Installiere RSA ETP Server auf $HOST_IP..."

# Kopiere Dateien zum Zielhost (mittels scp oder rsync)
scp -r "$SCRIPT_DIR"/* "user@$HOST_IP:/path/to/installation/"

echo "Installation abgeschlossen!"
