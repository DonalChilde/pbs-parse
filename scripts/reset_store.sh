STORE="$HOME/projects/tmp/store"
echo "***** Delete the old store. *****"
rm -rf $STORE
echo
echo "***** Create the store. *****"
echo
pbs-parse data-store create ~/projects/tmp/store November 2024-11-01 2024-12-01
echo
echo "***** Add the bid packages *****"
echo
pbs-parse data-store add-all-bases ~/projects/tmp/store ~/projects/tmp/pbs-data/2024.11.01-2024.12.01/
echo
echo "***** Parse the data *****"
echo
pbs-parse data-store parse-all ~/projects/tmp/store
