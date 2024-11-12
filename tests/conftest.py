import logging
from pathlib import Path

import pytest
from typer.testing import CliRunner


APP_LOG_LEVEL = logging.INFO
TEST_LOG_LEVEL = logging.DEBUG


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@pytest.fixture(scope="session", name="test_output_dir")
def test_output_dir_(tmp_path_factory: Path) -> Path:
    """make a temp directory for output data."""
    test_app_data_dir = tmp_path_factory.mktemp("pbs_parse")
    return test_app_data_dir


########################################################################
# Add an option to mark slow tests, so that they don't run every time. #
########################################################################


def pytest_addoption(parser):
    # https://docs.pytest.org/en/stable/example/simple.html#control-skipping-of-tests-according-to-command-line-option
    # conftest.py must be in the root test package.
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


# @pytest.fixture(scope="session", name="logger")
# def _logger(test_log_path: Path):
#     """A central logger that will log to file."""
#     log_dir: Path = test_log_path
#     handler = rotating_file_handler(
#         log_dir=log_dir,
#         file_name=__package__,
#         log_level=TEST_LOG_LEVEL,
#     )
#     test_logger = logging.getLogger(__package__)
#     test_logger.setLevel(TEST_LOG_LEVEL)
#     test_logger.addHandler(handler)
#     test_logger.info("Defined logger: %s", __package__)
#     test_logger.info(
#         "Rotating file logger %s initialized with handler= %r", __package__, handler
#     )
#     # project_logger = logging.getLogger("aa_pbs_exporter")
#     # add_handlers_to_target_logger(test_logger, project_logger)
#     # project_logger.setLevel(APP_LOG_LEVEL)
#     # test_logger.info("%s logs added to log file.", "aa_pbs_exporter")
#     return test_logger


@pytest.fixture(scope="session", name="test_log_path")
def test_log_path_(test_output_dir: Path) -> Path:
    """Make a test-log directory under the app data directory"""
    log_path = test_output_dir / Path("test-logs")
    print(f"Logging at: {log_path}")
    return log_path
