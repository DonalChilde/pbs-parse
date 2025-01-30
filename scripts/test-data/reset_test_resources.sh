#!/usr/bin/env bash
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
OUTPUT_DIR="$HOME/projects/tmp/test_resources/nov2024"
STORE_NAME="nov2024"
EFFECTIVE_FROM="2024-11-01"
EFFECTIVE_TO="2024-12-01"
INPUT_LOCATION="$HOME/projects/pbs-parse/tests/resources/eff_2024_11_01_2024_12_01/LAX/source/PBS_LAX_November_2024_20241010125833_partial.txt"

echo "***** Delete the old data at $OUTPUT_DIR. *****"
rm -rf $OUTPUT_DIR

pbs-parse manual split-to-pages "$INPUT_LOCATION" "$OUTPUT_DIR" "2024-11" "$EFFECTIVE_FROM" "$EFFECTIVE_TO" "LAX"

pbs-parse manual split-to-trips "$OUTPUT_DIR/LAX/pages" "$OUTPUT_DIR/LAX/trip_lines"

pbs-parse manual parse "$OUTPUT_DIR/LAX/trip_lines" "$OUTPUT_DIR/LAX/parsed"

pbs-parse manual expand "$OUTPUT_DIR/LAX/parsed" "$OUTPUT_DIR/LAX/expanded" "--debug-dir=$OUTPUT_DIR/LAX/expanded/debug"
