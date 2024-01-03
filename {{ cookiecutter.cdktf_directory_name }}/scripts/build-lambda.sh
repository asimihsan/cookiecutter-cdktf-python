#!/usr/bin/env bash

# This script builds a Docker image for a specified lambda function.
# It accepts command-line arguments to specify the lambda folder name
# and the Docker image name with tag.

# Usage:
# ./build-lambda.sh --lambda-folder <folder_name> --image-name <image_name:tag>

set -euo pipefail

# Function to display usage information
usage() {
    echo "Usage: $0 --lambda-folder <folder_name> --image-name <image_name:tag>"
    exit 1
}

# Initialize variables with default values
LAMBDA_FOLDER="lambda_python"
IMAGE_NAME="lambda-python:latest"

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --lambda-folder) LAMBDA_FOLDER="$2"; shift ;;
        --image-name) IMAGE_NAME="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; usage ;;
    esac
    shift
done

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# Get the root directory of the project
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
# Find the directory of the lambda function
LAMBDA_PYTHON_DIR=$(find "$ROOT_DIR/src" -type d -name "$LAMBDA_FOLDER")

# Check if the lambda directory exists and contains a Dockerfile
if [[ -d "$LAMBDA_PYTHON_DIR" && -f "$LAMBDA_PYTHON_DIR/Dockerfile" ]]; then
    # Change to the lambda directory
    pushd "$LAMBDA_PYTHON_DIR"
    # Ensure we return to the original directory when the script exits
    trap "popd 2>&1 > /dev/null" EXIT

    # Build the Docker image
    docker buildx build --platform linux/arm64 -t "$IMAGE_NAME" . --load
else
    echo "Error: The specified lambda folder does not exist or does not contain a Dockerfile."
    exit 1
fi
