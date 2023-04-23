#! /usr/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/build-image.sh"
source "$SCRIPT_DIR/push-image.sh"
source "$SCRIPT_DIR/redeploy-latest-task-service.sh"

