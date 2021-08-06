import pytest
import numpy as np

from environment.env import Direction
from game.core.grid import Food
from game.core.grid import Snake
from game.core.grid import Grid

@pytest.fixture
def food():
    return Food(100, 100, np.array([1, 1]))

def test_start_position(food):
    assert (food.position() == np.array([1, 1])).all()

def test_move(food):
    food.move(np.array([10, 10]))
    assert (food.position() == np.array([10, 10])).all()


@pytest.fixture
def snake():
    start_position = np.array([10, 10])
    return Snake(start_position=start_position, direction=Direction.UP, snake_size=1, grid_slots=20)

def test_get_snake_head_initial(snake):
    assert (snake.head() == np.array([10, 10])).all()

def test_move_snake_illegal_direction(snake):
    new_head = snake.move(direction=Direction.DOWN)
    assert (new_head == np.array([10, 11])).all()
    assert snake.length() == 1

def test_move_snake_legal_direction(snake):
    new_head = snake.move(direction=Direction.LEFT)
    assert (new_head == np.array([9, 10])).all()
    assert snake.length() == 1

def test_move_snake_multiple_directions(snake):
    snake.move(direction=Direction.UP)
    snake.move(direction=Direction.UP)
    snake.move(direction=Direction.LEFT)
    new_head = snake.move(direction=Direction.DOWN)
    assert (new_head == np.array([9, 9])).all()
    assert snake.length() == 1

def test_length_position_snake_add_tail(snake):
    new_head = snake.move(direction=Direction.LEFT, add_tail=True)
    assert (new_head == np.array([9, 10])).all()
    assert snake.length() == 2

def test_snake_body(snake):
    snake.move(direction=Direction.LEFT, add_tail=True)
    assert (snake.position() == np.array([[9, 10], [10, 10]])).all()
    assert snake.length() == 2

def test_snake_touches_tail_no_tail(snake):
    assert snake.touches_tail() == False

def test_snake_touches_tail(snake):
    snake.move(direction=Direction.UP, add_tail=True)
    snake.move(direction=Direction.LEFT, add_tail=True)
    snake.move(direction=Direction.DOWN, add_tail=True)
    snake.move(direction=Direction.RIGHT, add_tail=True)
    assert snake.touches_tail() == True
