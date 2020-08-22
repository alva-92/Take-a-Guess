import pytest
from mock import patch
import module
import GuessGame


dfclty_cases = [1,2,3]

@pytest.mark.parametrize('test_input', dfclty_cases)
def test_config_game(monkeypatch, test_input):
    monkeypatch.setattr('builtins.input', lambda _: test_input)
    test_inst = GuessGame.GuessGame()
    result = test_inst.configure_game()
    assert isinstance(result, int) and result >= 1 and result <= 3