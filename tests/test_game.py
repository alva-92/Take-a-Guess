"""
    Package integration and unit tests.
"""

import pytest
from mock import patch
import module
from .context import GuessGame
from .context import gameSettings

dfclty_cases_success = ['1','2','3']
dfclty_cases_fail    = ['0', 'a', '@', '4']

@pytest.mark.parametrize('test_input', dfclty_cases_success)
def test_config_game_s(monkeypatch, test_input):
    monkeypatch.setattr('builtins.input', lambda _: test_input)
    test_inst = GuessGame()
    result = test_inst.configure_game()
    assert result == gameSettings.SUCCESS

@pytest.mark.parametrize('test_input', dfclty_cases_fail)
def test_config_game_f(monkeypatch, test_input):
    monkeypatch.setattr('builtins.input', lambda _: test_input)
    test_inst = GuessGame()
    result = test_inst.configure_game()
    assert result == gameSettings.INVALID_DIFFICULTY

