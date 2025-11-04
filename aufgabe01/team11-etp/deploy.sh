#!/bin/env bash
USER=$1

if [ -z $USER ];then
    echo "bitte gib ein username ein"
    exit 1
fi
cd ../

echo "Tar datei in /tmp erstellt"
tar -cf /tmp/team11-etp.tar team11-etp


echo "tar datei in server geschoben"
scp /tmp/team11-etp.tar $USER@10.42.2.111:~/


echo "tar datei extrhiert"
ssh "$USER@10.42.2.111" "tar -xf ~/team11-etp.tar"