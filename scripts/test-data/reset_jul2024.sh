#!/usr/bin/env bash
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
STORE_NAME="jul2024"
EFFECTIVE_FROM="2024-07-02"
EFFECTIVE_TO="2024-07-31"
INPUT_LOCATION="$HOME/projects/tmp/pbs-data/2024-07-02_2024-07-31"

$SCRIPT_DIR/reset_store.sh "$STORE_NAME" "$EFFECTIVE_FROM" "$EFFECTIVE_TO" "$INPUT_LOCATION"
