#!/usr/bin/env bash

set -e # stop on errors

# We want to be able to roll forward and backward, and keep a history of our images
# for troubleshooting. To do that, we're just adding a YYYYMMDDHHMMSS timestamp
# to our images.

version=$(date '+%Y%m%d%H%M%S')
repository="savvlydeveastus.azurecr.io/fmv"

#sudo chmod 666 /var/run/docker.sock

docker build --no-cache -t "${repository}:${version}" .

echo "Image '${repository}:${version}' has been built. You can now 'docker push ${repository}:${version}'"

