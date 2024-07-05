#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

export GIT_SERVER_HOME_DIR="${GIT_SERVER_HOME_DIR:-/app/sdic/git/home}"
export GIT_CONTAINER_NAME="${GIT_CONTAINER_NAME:-sdic-git}"
export GIT_SEVER_PORT="${GIT_SEVER_PORT:-2256}"
export GIT_SERVER_BUILD_IMAGE_NAME="${GIT_SERVER_BUILD_IMAGE_NAME:-sdic-git}"
export GIT_SERVER_BUILD_IMAGE_TAG="${GIT_SERVER_BUILD_IMAGE_TAG:-latest}"

echo "Creating git server home directory: ${GIT_SERVER_HOME_DIR}"
mkdir -p "${GIT_SERVER_HOME_DIR}"

echo "Removing existing container and image"
docker rm -f "${GIT_CONTAINER_NAME}"
docker rmi -f "${GIT_SERVER_BUILD_IMAGE_NAME}:${GIT_SERVER_BUILD_IMAGE_TAG}" || true

echo "Building git server image"
docker buildx build -t "${GIT_SERVER_BUILD_IMAGE_NAME}:${GIT_SERVER_BUILD_IMAGE_TAG}" -f Dockerfile . \
    --progress=plain --no-cache

echo "Running git server container"
docker run -d --name "${GIT_CONTAINER_NAME}" \
    -v "${GIT_SERVER_HOME_DIR}:/git-server" \
    --restart=unless-stopped \
    -p "${GIT_SEVER_PORT}:22" \
    "${GIT_SERVER_BUILD_IMAGE_NAME}:${GIT_SERVER_BUILD_IMAGE_TAG}"
