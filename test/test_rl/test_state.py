import pytest

from game.snake import SnakeGame
from rl.state import SnakeState3

import numpy as np

@pytest.fixture
def snake_state_3():
    game = SnakeGame(200, 200, 20)

    state = SnakeState3(game)
    return state

@pytest.fixture
def vicinity():
    return np.array([[4, 5], [5, 4], [6, 5]])

@pytest.fixture
def snake_body():
    return np.array([[5, 5]])


def test_get_danger(snake_state_3, vicinity, snake_body):
    assert(snake_state_3.get_danger(vicinity, snake_body) == np.array([0, 0, 0])).all()