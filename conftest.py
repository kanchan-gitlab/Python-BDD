from pathlib import Path

import pytest

from utils.helper import get_current_time


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # set custom options only if none are provided from command line
    if not config.option.htmlpath:
        now = get_current_time()
        # create report target dir
        results_dir = Path('results', now.strftime('%Y%m%d'))
        results_dir.mkdir(parents=True, exist_ok=True)
        # custom report file
        results = results_dir / f"report_{now.strftime('%H%M%S')}.html"
        # adjust plugin options
        config.option.htmlpath = results
        config.option.self_contained_html = True


@pytest.fixture
def context():
    # returns empty dict
    return {}
