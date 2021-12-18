#!/bin/bash

# GET ARTIFACT NAME Script
# This script generates the names for the image artifacts used in certain jobs.
#
# Two artifacts are used:
# - Digest artifacts: they hold the last know Digest from each Base Image used.
# - Image Changed flag: used only for letting the build job know if the image based on a certain Base Image must be built. Its content is irrelevant.
#
# Inputs: environment variables:
# - BASEIMAGE: full base image name, in format author/name:tag (or name:tag for official images)
# - ARCH: image arch
#
# Outputs (GITHUB_ENV):
# - digestArtifactName
# - imageChangedArtifactName

set -e

function setOutput() {
  # Echo for setting an environment variable on GITHUB_ENV
  # $1=key, $2=value
  echo "$1=$2" >> $GITHUB_ENV
}

function stringSafe() {
  # Escape the following characters from digestArtifactName with "-":    " : < > | * ? \ /
  ESCAPE_CHARS="\":<>|*?\\\/"
  REPLACE_WITH="-"
  echo "$1" | tr "$ESCAPE_CHARS" "$REPLACE_WITH"
}

test "$BASEIMAGE" || { echo "No BASEIMAGE env var defined!"; exit 1; }
test "$ARCH" || { echo "No ARCH env var defined!"; exit 1; }

set -ex

digestArtifactName="digest-$BASEIMAGE-$ARCH"
imageChangedArtifactName="imageChanged-$BASEIMAGE-$ARCH"

digestArtifactName=$(stringSafe "$digestArtifactName")
imageChangedArtifactName=$(stringSafe "$imageChangedArtifactName")

setOutput "digestArtifactName" "$digestArtifactName"
setOutput "imageChangedArtifactName" "$imageChangedArtifactName"
