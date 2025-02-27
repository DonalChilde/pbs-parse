#!/usr/bin/env bash

set -euo pipefail
TIMEFORMAT='Tasks compeleted in  %R seconds...'
time {
    SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
    STATS_FILE="$HOME/projects/tmp/stats-all.txt"
    STD_CAP_DIR="$HOME/projects/tmp/reset-cap-logs"
    rm -rf $STD_CAP_DIR
    mkdir $STD_CAP_DIR
    echo "**** Resetting all bids ****"

    "$SCRIPT_DIR/reset_jan2024.sh" >"$STD_CAP_DIR/jan2024-stdout.txt" 2>"$STD_CAP_DIR/jan2024-stderr.txt" &
    "$SCRIPT_DIR/reset_feb2024.sh" >"$STD_CAP_DIR/feb2024-stdout.txt" 2>"$STD_CAP_DIR/feb2024-stderr.txt" &
    "$SCRIPT_DIR/reset_mar2024.sh" >"$STD_CAP_DIR/mar2024-stdout.txt" 2>"$STD_CAP_DIR/mar2024-stderr.txt" &
    "$SCRIPT_DIR/reset_apr2024.sh" >"$STD_CAP_DIR/apr2024-stdout.txt" 2>"$STD_CAP_DIR/apr2024-stderr.txt" &
    "$SCRIPT_DIR/reset_may2024.sh" >"$STD_CAP_DIR/may2024-stdout.txt" 2>"$STD_CAP_DIR/may2024-stderr.txt" &
    "$SCRIPT_DIR/reset_jun2024.sh" >"$STD_CAP_DIR/jun2024-stdout.txt" 2>"$STD_CAP_DIR/jun2024-stderr.txt" &
    "$SCRIPT_DIR/reset_jul2024.sh" >"$STD_CAP_DIR/jul2024-stdout.txt" 2>"$STD_CAP_DIR/jul2024-stderr.txt" &
    "$SCRIPT_DIR/reset_aug2024.sh" >"$STD_CAP_DIR/aug2024-stdout.txt" 2>"$STD_CAP_DIR/aug2024-stderr.txt" &
    "$SCRIPT_DIR/reset_sep2024.sh" >"$STD_CAP_DIR/sep2024-stdout.txt" 2>"$STD_CAP_DIR/sep2024-stderr.txt" &
    "$SCRIPT_DIR/reset_oct2024.sh" >"$STD_CAP_DIR/oct2024-stdout.txt" 2>"$STD_CAP_DIR/oct2024-stderr.txt" &
    "$SCRIPT_DIR/reset_nov2024.sh" >"$STD_CAP_DIR/nov2024-stdout.txt" 2>"$STD_CAP_DIR/nov2024-stderr.txt" &
    "$SCRIPT_DIR/reset_dec2024.sh" >"$STD_CAP_DIR/dec2024-stdout.txt" 2>"$STD_CAP_DIR/dec2024-stderr.txt" &
    "$SCRIPT_DIR/reset_2025-01.sh" >"$STD_CAP_DIR/2025-01-stdout.txt" 2>"$STD_CAP_DIR/2025-01-stderr.txt" &
    "$SCRIPT_DIR/reset_2025-02.sh" >"$STD_CAP_DIR/2025-02-stdout.txt" 2>"$STD_CAP_DIR/2025-02-stderr.txt" &
    "$SCRIPT_DIR/reset_2025-03.sh" >"$STD_CAP_DIR/2025-03-stdout.txt" 2>"$STD_CAP_DIR/2025-03-stderr.txt" &
    wait

    "$SCRIPT_DIR/stats_all.sh" >"$STATS_FILE"
}
