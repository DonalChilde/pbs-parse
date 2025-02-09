#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
STORES_DIR="$HOME/projects/tmp/stores"
STORE_NAME=("jan2024" "feb2024" "mar2024" "apr2024" "may2024" "jun2024" "jul2024" "aug2024" "sep2024" "oct2024" "nov2024" "dec2024" "2025-01" "2025-02" "2025-03")

for store in ${STORE_NAME[@]}; do
    pbs-parse store stats $STORES_DIR/$store
done
