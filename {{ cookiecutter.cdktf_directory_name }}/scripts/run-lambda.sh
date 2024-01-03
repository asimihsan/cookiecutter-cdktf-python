#!/usr/bin/env bash

IMAGE_NAME=lambda-python
TAG=latest

docker run --platform linux/arm64 -p 9000:8080 \
    -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    -e AWS_SESSION_TOKEN="${AWS_SESSION_TOKEN}" \
    -e AWS_REGION="${AWS_REGION}" \
    "${IMAGE_NAME}:${TAG}"
