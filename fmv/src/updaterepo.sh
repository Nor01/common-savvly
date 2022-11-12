#!/bin/sh
#set -x
#trap read debug
if [ -z "$1" ]; then
    echo "Missing Parameter: Pass the text to be added to commit"
    exit 0
fi

cd common
git commit -a -m \'"$@"\'
git push origin HEAD:master
cd ..
git submodule update --recursive --remote
git commit -a -m \'"$@"\'
git push