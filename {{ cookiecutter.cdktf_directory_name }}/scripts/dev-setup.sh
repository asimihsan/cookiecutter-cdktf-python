#!/usr/bin/env bash

set -euo pipefail

# Function to log messages with a timestamp
log() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] $1"
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
pushd "$ROOT_DIR" >/dev/null
trap "popd > /dev/null" EXIT

install_pre_commit() {
    if command -v pre-commit &>/dev/null; then
        log "pre-commit is already installed."
    else
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install pre-commit
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt update
            sudo apt install -y pre-commit
        else
            log "Unsupported OS for pre-commit installation."
            exit 1
        fi
    fi
    pre-commit install
}

install_cdktf_cli() {
    if command -v cdktf &>/dev/null; then
        log "cdktf-cli is already installed."
    else
        brew install cdktf
    fi
}

install_poetry_dependencies() {
    if ! poetry install --with=dev --no-root; then
        log "poetry install failed."
        exit 1
    fi
}

install_pre_commit
install_cdktf_cli
install_poetry_dependencies

# Find subdirs with pyproject.toml in root, iterate over them
while IFS= read -r d; do
    log "Installing poetry dependencies for $d"
    (cd "$d" && poetry install --with=dev --no-root)
done < <(find . -name "pyproject.toml" -exec dirname {} \;)

# Check if awscurl is installed via Homebrew and install if not
if [[ "$OSTYPE" == "darwin"* ]]; then
    if brew list awscurl &>/dev/null; then
        log "awscurl is already installed via Homebrew."
    else
        brew install awscurl
    fi
else
    log "awscurl installation is only supported on macOS via Homebrew."
fi
