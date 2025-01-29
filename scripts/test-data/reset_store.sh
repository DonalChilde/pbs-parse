#!/usr/bin/env bash
# Argument validation check
if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <stores_dir> <store_name> <effective_from> <effective_to> <input location>"
    exit 1
fi
STORES_DIR=$1
STORE_NAME=$2
EFFECTIVE_FROM=$3
EFFECTIVE_TO=$4
INPUT_LOCATION=$5
STORE="$STORES_DIR/$STORE_NAME"
DEBUG_DIR="$HOME/projects/tmp/store-debug"

echo "***** Delete the old store at $STORE. *****"
rm -rf $STORE
echo
echo "***** Create the store. *****"
echo
pbs-parse create-store "$STORE" "$STORE_NAME" "$EFFECTIVE_FROM" "$EFFECTIVE_TO"
echo
echo "***** Add the bid packages *****"
echo
pbs-parse store add-all-bases $STORE $INPUT_LOCATION
echo
echo "***** Parse the data *****"
echo
pbs-parse store do $STORE _all_
echo
echo "***** Generating $STORE_NAME-stats.txt"
echo
pbs-parse store stats "$STORE" ">" "$STORE/$STORE_NAME-stats.txt"
echo
echo "***** Exporting expanded trip debug data *****"
pbs-parse store export expanded-debug "$STORE" "$DEBUG_DIR"
echo
