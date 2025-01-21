#!/usr/bin/env bash
# https://stackoverflow.com/a/4494535
# https://dateful.com/convert/utc

# ERROR_TRIPS top level dir of the PageLines.json containing errors.
# Expects bases in subdirs.
# Assumes all are from the same bid period.
# All stages are output to the BASE/parsed directory, to make it easier to see whole picture,
# And to keep cli command small on validation steps.
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
    pbs-parse manual structure "$ERROR_TRIPS/$dir/parsed" "$ERROR_TRIPS/$dir/parsed"
    pbs-parse manual validate-structured "$ERROR_TRIPS/$dir/parsed" "$ERROR_TRIPS/$dir/parsed/errors"
    pbs-parse manual expand "$ERROR_TRIPS/$dir/parsed" "$ERROR_TRIPS/$dir/parsed"
    pbs-parse manual validate-expanded "$ERROR_TRIPS/$dir/parsed" "$ERROR_TRIPS/$dir/parsed/errors"
done
