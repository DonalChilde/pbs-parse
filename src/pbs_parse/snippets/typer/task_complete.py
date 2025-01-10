"""task_complete.py."""

from time import perf_counter_ns

import typer


def task_complete(start_perf: int):
    """Output a task complete message with elapsed time.

    Args:
        start_perf (int): An int from perf_counter_ns().
    """
    end_perf = perf_counter_ns()
    length = end_perf - start_perf
    typer.echo(f"\nTask completed in {length/1000000000:9f} seconds.")
