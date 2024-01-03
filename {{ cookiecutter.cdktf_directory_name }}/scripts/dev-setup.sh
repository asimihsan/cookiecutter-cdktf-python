#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
pushd "$ROOT_DIR" >/dev/null
trap "popd > /dev/null" EXIT

install_pre_commit() {
    if command -v pre-commit &>/dev/null; then
        echo "pre-commit is already installed."
    else
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install pre-commit
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt update
            sudo apt install -y pre-commit
        else
            echo "Unsupported OS for pre-commit installation."
            exit 1
        fi
    fi
    pre-commit install
}

install_pre_commit

npm install --global cdktf-cli@latest
npm install
poetry install --with=dev --no-root

# Find subdirs with pyproject.toml in root, iterate over them
while IFS= read -r d; do
    echo "Installing poetry dependencies for $d"
    (cd "$d" && poetry install --with=dev --no-root)
done < <(find . -name "pyproject.toml" -exec dirname {} \;)

brew install awscurl
