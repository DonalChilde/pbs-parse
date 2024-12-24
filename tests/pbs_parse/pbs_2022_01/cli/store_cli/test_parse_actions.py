"""FILE: test_parse_actions.py."""

import pytest

from pbs_parse.cli.store_cli.common import ParseActions


def test_action_list():
    """test_action_list."""
    full_list = ParseActions.action_list(
        start=ParseActions.SPLIT_TO_PAGES, end=ParseActions.EXPAND_TRIPS
    )
    assert full_list[-1] == ParseActions.EXPAND_TRIPS

    with pytest.raises(ValueError):
        _ = ParseActions.action_list(
            ParseActions.EXPAND_TRIPS, ParseActions.SPLIT_TO_TRIPS
        )

    partial_list = ParseActions.action_list(
        ParseActions.SPLIT_TO_TRIPS, ParseActions.STRUCTURE_TRIPS
    )
    assert partial_list[0] == ParseActions.SPLIT_TO_TRIPS
    assert partial_list[-1] == ParseActions.STRUCTURE_TRIPS
    assert len(partial_list) == 3
