import pytest

from ..src.loader import *


def test_pytest_works():
    log_loader = loader.LogLoader()
    # log_loader.load_log_snapshot('../data/frozen_output.log')
    assert True