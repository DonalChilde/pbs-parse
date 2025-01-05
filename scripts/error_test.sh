#!/usr/bin/env bash
# https://stackoverflow.com/a/4494535
# https://dateful.com/convert/utc
ERROR_TRIPS="$HOME/projects/tmp/error-trips"
BID_PERIOD="2024-11-01 2024-12-01"
readarray -t dirs < <(find $ERROR_TRIPS -mindepth 1 -maxdepth 1 -type d -printf '%P\n')

# remove last parse
for dir in "${dirs[@]}"; do
    rm -rf "$ERROR_TRIPS/$dir/parsed"
done

for dir in "${dirs[@]}"; do
    pbs-parse manual split-to-trips "$ERROR_TRIPS/$dir" "$ERROR_TRIPS/$dir/parsed"
    pbs-parse manual parse "$ERROR_TRIPS/$dir/parsed" "$ERROR_TRIPS/$dir/parsed"
    pbs-parse manual structure "$ERROR_TRIPS/$dir/parsed" "$ERROR_TRIPS/$dir/parsed" $BID_PERIOD
    pbs-parse manual validate-structured "$ERROR_TRIPS/$dir/parsed" "$ERROR_TRIPS/$dir/parsed/errors"
    pbs-parse manual expand "$ERROR_TRIPS/$dir/parsed" "$ERROR_TRIPS/$dir/parsed"
    pbs-parse manual validate-expanded "$ERROR_TRIPS/$dir/parsed" "$ERROR_TRIPS/$dir/parsed/errors"
done
