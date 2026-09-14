import pytest

from backtracking_puzzles.maze_solver import solve_maze


def _is_valid_path(grid, path, start, end):
    if path[0] != start or path[-1] != end:
        return False
    for r, c in path:
        if grid[r][c] != 0:
            return False
    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            return False
    return len(set(path)) == len(path)


class TestSolvableMaze:
    def test_simple_straight_path(self):
        grid = [
            [0, 0, 0],
            [1, 1, 0],
            [0, 0, 0],
        ]
        start, end = (0, 0), (2, 2)
        path = solve_maze(grid, start, end)
        assert path is not None
        assert _is_valid_path(grid, path, start, end)

    def test_open_grid_start_equals_end(self):
        grid = [[0, 0], [0, 0]]
        path = solve_maze(grid, (0, 0), (0, 0))
        assert path == [(0, 0)]


class TestUnsolvableMaze:
    def test_completely_walled_off_target(self):
        grid = [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
        ]
        path = solve_maze(grid, (0, 0), (0, 2))
        assert path is None

    def test_no_path_around_a_box(self):
        grid = [
            [0, 1, 1],
            [1, 1, 1],
            [0, 1, 0],
        ]
        path = solve_maze(grid, (0, 0), (2, 2))
        assert path is None


class TestInvalidInput:
    def test_start_out_of_bounds_raises(self):
        grid = [[0, 0], [0, 0]]
        with pytest.raises(ValueError):
            solve_maze(grid, (5, 5), (0, 0))

    def test_end_on_wall_raises(self):
        grid = [[0, 1], [0, 0]]
        with pytest.raises(ValueError):
            solve_maze(grid, (0, 0), (0, 1))

    def test_start_on_wall_raises(self):
        grid = [[1, 0], [0, 0]]
        with pytest.raises(ValueError):
            solve_maze(grid, (0, 0), (1, 1))
