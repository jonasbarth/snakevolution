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
    return Snake(start_position=start_position, direction=Direction.STRAIGHT, snake_size=1, grid_slots=20)

def test_get_snake_head_initial(snake):
    assert (snake.head() == np.array([10, 10])).all()

def test_move_snake_legal_direction(snake):
    new_head = snake.move(direction=Direction.LEFT)
    assert (new_head == np.array([9, 10])).all()
    assert snake.length() == 1

def test_move_snake_multiple_directions(snake):
    snake.move(direction=Direction.STRAIGHT)
    snake.move(direction=Direction.STRAIGHT)
    snake.move(direction=Direction.LEFT)
    new_head = snake.move(direction=Direction.STRAIGHT)
    assert (new_head == np.array([8, 8])).all()
    assert snake.length() == 1

def test_length_position_snake_add_tail_left(snake):
    new_head = snake.move(direction=Direction.LEFT, add_tail=True)
    assert (new_head == np.array([9, 10])).all()
    assert snake.length() == 2

def test_length_position_snake_add_tail_right(snake):
    new_head = snake.move(direction=Direction.RIGHT, add_tail=True)
    assert (new_head == np.array([11, 10])).all()
    assert snake.length() == 2

def test_snake_body(snake):
    snake.move(direction=Direction.LEFT, add_tail=True)
    assert (snake.position() == np.array([[9, 10], [10, 10]])).all()
    assert snake.length() == 2

def test_snake_touches_tail_no_tail(snake):
    assert snake.touches_tail() == False

def test_snake_touches_tail(snake):
    snake.move(direction=Direction.STRAIGHT, add_tail=True)
    snake.move(direction=Direction.LEFT, add_tail=True)
    snake.move(direction=Direction.LEFT, add_tail=True)
    snake.move(direction=Direction.LEFT, add_tail=True)
    assert snake.touches_tail() == True

def test_snake_initial_vicinity(snake):
    assert (snake.vicinity() == np.array([[10, 9], [9, 10], [11, 10]])).all()

def test_snake_vicinity_after_left_move(snake):
    snake.move(direction=Direction.LEFT, add_tail=True)
    assert (snake.vicinity() == np.array([[8, 10], [9, 11], [9, 9]])).all()

def test_snake_vicinity_after_right_move(snake):
    snake.move(direction=Direction.RIGHT, add_tail=True)
    assert (snake.vicinity() == np.array([[12, 10], [11, 9], [11, 11]])).all()




@pytest.fixture
def grid():
    return Grid(10, 10)

def test_snake_start_position_in_middle(grid):
    assert (grid.start_position() == np.array([5, 5])).all()

def test_move_snake(grid):
    assert (grid.move_snake(Direction.STRAIGHT, False) == np.array([5, 4])).all()
    assert (grid.move_snake(Direction.LEFT, False) == np.array([4, 4])).all()
    assert (grid.move_snake(Direction.STRAIGHT, False) == np.array([3, 4])).all()

def test_move_food(grid):
    assert(grid.move_food(np.array([1, 3])) == np.array([1, 3])).all()
    assert(grid.food().position() == np.array([1, 3])).all()

def test_make_snake_win():
    grid = Grid(2, 2)
    grid.move_snake(Direction.STRAIGHT, True)
    grid.move_snake(Direction.LEFT, True)
    #grid.move_snake(Direction.LEFT, True)
    grid.move_snake(Direction.LEFT, True)
    assert(grid.available_slots().size == 0)

def test_set_snake_in_grid(grid):
    grid.move_snake(Direction.LEFT, False)
    grid.set_snake_in_grid()
    assert(grid.grid[5][4] == 1)

def test_set_food_in_grid(grid):
    grid.set_food_in_grid()
    food_x, food_y = grid.food().position()
    assert(grid.grid[food_y][food_x] == 2)

def test_coordinate_inside_grid(grid):
    for x in range(10):
        for y in range(10):
            coordinates = np.array([x, y])
            assert(grid.is_outside_grid(coordinates) == False)

def test_coordinate_outside_grid(grid):
    for x in range(10, 20):
        for y in range(10, 20):
            coordinates = np.array([x, y])
            assert(grid.is_outside_grid(coordinates) == True)

def test_legal_coordinates(grid):
    assert(grid.compute_legal_coordinates(2, 2) == np.array([[0, 0], [0, 1], [1, 0], [1, 1]])).all()

def test_available_slots():
    grid = Grid(2, 2)
    assert(grid.available_slots().shape[0] == 2)
    grid.move_snake(Direction.STRAIGHT, True)
    grid.move_food(grid.random_food())
    assert (grid.available_slots().shape[0] == 1)
    grid.move_snake(Direction.LEFT, True)
    grid.move_food(grid.random_food())
    assert (grid.available_slots().shape[0] == 0)

