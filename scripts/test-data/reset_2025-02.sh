#!/usr/bin/env bash
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
STORES_DIR="$HOME/projects/tmp/stores"
STORE_NAME="2025-02"
EFFECTIVE_FROM="2025-01-31"
EFFECTIVE_TO="2025-03-01"
INPUT_LOCATION="$HOME/projects/tmp/pbs-data/2025-01-31_2025-03-01"

$SCRIPT_DIR/reset_store.sh "$STORES_DIR" "$STORE_NAME" "$EFFECTIVE_FROM" "$EFFECTIVE_TO" "$INPUT_LOCATION"
