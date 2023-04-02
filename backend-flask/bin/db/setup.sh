#!/usr/bin/bash -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/drop.sh"
source "$SCRIPT_DIR/create.sh"
source "$SCRIPT_DIR/load-schema.sh"
source "$SCRIPT_DIR/seed.sh"
