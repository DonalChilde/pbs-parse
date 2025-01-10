#!/usr/bin/env bash
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
STORE_NAME="mar2024"
EFFECTIVE_FROM="2024-03-02"
EFFECTIVE_TO="2024-03-31"
INPUT_LOCATION="$HOME/projects/tmp/pbs-data/2024-03-02_2024-03-31"

$SCRIPT_DIR/reset_store.sh "$STORE_NAME" "$EFFECTIVE_FROM" "$EFFECTIVE_TO" "$INPUT_LOCATION"
