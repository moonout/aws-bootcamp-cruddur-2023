#!/usr/bin/bash -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/db-drop.sh"
source "$SCRIPT_DIR/db-create.sh"
source "$SCRIPT_DIR/db-load-schema.sh"
source "$SCRIPT_DIR/db-seed.sh"
