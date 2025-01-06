#!/usr/bin/env bash
# Argument validation check
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <store name> <effective_from> <effective_to> <input location>"
    exit 1
fi
STORES_DIR="$HOME/projects/tmp/stores"
STORE_NAME=$1
EFFECTIVE_FROM=$2
EFFECTIVE_TO=$3
INPUT_LOCATION=$4
STORE="$STORES_DIR/$STORE_NAME"

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
