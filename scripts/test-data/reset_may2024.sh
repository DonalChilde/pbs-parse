#!/usr/bin/env bash
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
STORES_DIR="$HOME/projects/tmp/stores"
STORE_NAME="may2024"
EFFECTIVE_FROM="2024-05-02"
EFFECTIVE_TO="2024-06-01"
INPUT_LOCATION="$HOME/projects/tmp/pbs-data/2024-05-02_2024-06-01"

$SCRIPT_DIR/reset_store.sh "$STORES_DIR" "$STORE_NAME" "$EFFECTIVE_FROM" "$EFFECTIVE_TO" "$INPUT_LOCATION"
