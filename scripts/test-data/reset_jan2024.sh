#!/usr/bin/env bash
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
STORES_DIR="$HOME/projects/tmp/stores"
STORE_NAME="jan2024"
EFFECTIVE_FROM="2024-01-01"
EFFECTIVE_TO="2024-01-30"
INPUT_LOCATION="$HOME/projects/tmp/pbs-data/2024-01-01_2024-01-30"

$SCRIPT_DIR/reset_store.sh "$STORES_DIR" "$STORE_NAME" "$EFFECTIVE_FROM" "$EFFECTIVE_TO" "$INPUT_LOCATION"
