#!/usr/bin/env bash

# This script tags a Docker image and pushes it to an AWS ECR repository.
# It accepts command-line arguments to specify the image name, tag, and AWS region.

# Usage:
# ./push_to_ecr.sh --image-name <image_name> --tag <tag> --region <aws_region>

set -euo pipefail

# Function to display usage information
usage() {
    echo "Usage: $0 --image-name <image_name> --tag <tag> --region <aws_region>"
    exit 1
}

# Initialize variables with default values
IMAGE_NAME="lambda-python"
TAG="latest"
REGION="{{ cookiecutter.aws_region }}" # Default AWS region

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --image-name) IMAGE_NAME="$2"; shift ;;
        --tag) TAG="$2"; shift ;;
        --region) REGION="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; usage ;;
    esac
    shift
done

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Get the root directory of the project
ROOT_DIR="$( cd "${SCRIPT_DIR}/.." && pwd )"
# Define the path to the outputs.json file
OUTPUTS_JSON_FILE="${ROOT_DIR}/ecr-repo-outputs.json"

# Check if the outputs.json file exists
if [ ! -f "${OUTPUTS_JSON_FILE}" ]; then
  echo "Outputs file not found: ${OUTPUTS_JSON_FILE}, run 'make cdktf-output' first"
  exit 1
fi

# Extract the ECR repository URL from the outputs.json file
ECR_REPO_URL=$(jq -r '.["ecr-repo"]["ecr_repo_repository_url"]' "${OUTPUTS_JSON_FILE}")
echo "ECR Repo URL: ${ECR_REPO_URL}"

# Log in to the ECR repository
aws ecr get-login-password --region "${REGION}" | docker login --username AWS --password-stdin "${ECR_REPO_URL}"

# Tag the Docker image with the ECR repository URL and the specified tag
docker tag "${IMAGE_NAME}:${TAG}" "${ECR_REPO_URL}:${IMAGE_NAME}-${TAG}"

# Push the tagged image to the ECR repository
docker push "${ECR_REPO_URL}:${IMAGE_NAME}-${TAG}"
