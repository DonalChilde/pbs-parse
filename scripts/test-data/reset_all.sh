#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
STATS_FILE="$HOME/projects/tmp/stats-all.txt"
echo "**** Resetting all bids ****"

"$SCRIPT_DIR/reset_jan2024.sh"
"$SCRIPT_DIR/reset_feb2024.sh"
"$SCRIPT_DIR/reset_mar2024.sh"
"$SCRIPT_DIR/reset_apr2024.sh"
"$SCRIPT_DIR/reset_may2024.sh"
"$SCRIPT_DIR/reset_jun2024.sh"
"$SCRIPT_DIR/reset_jul2024.sh"
"$SCRIPT_DIR/reset_aug2024.sh"
"$SCRIPT_DIR/reset_sep2024.sh"
"$SCRIPT_DIR/reset_oct2024.sh"
"$SCRIPT_DIR/reset_nov2024.sh"
"$SCRIPT_DIR/reset_dec2024.sh"
"$SCRIPT_DIR/reset_2025-01.sh"
"$SCRIPT_DIR/reset_2025-02.sh"

"$SCRIPT_DIR/stats_all.sh" >"$STATS_FILE"
