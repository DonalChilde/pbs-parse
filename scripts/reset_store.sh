#!/usr/bin/env bash
STORE="$HOME/projects/tmp/store"
echo "***** Delete the old store. *****"
rm -rf $STORE
echo
echo "***** Create the store. *****"
echo
pbs-parse create-store $STORE November 2024-11-01 2024-12-01
echo
echo "***** Add the bid packages *****"
echo
pbs-parse store add-all-bases $STORE ~/projects/tmp/pbs-data/2024-11-01_2024-12-01/
echo
echo "***** Parse the data *****"
echo
pbs-parse store do ~/projects/tmp/store _all_
