"""Tests for the Try It Yourself solutions in facit/prova_sjalv.py."""

from itertools import permutations
from math import factorial

import pytest

from backtracking_puzzles.maze_solver import solve_maze
from facit import prova_sjalv as facit

OPEN_GRID = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
# A ring around a 2x2 wall: two equally long routes from corner to corner.
DETOUR_GRID = [
    [0, 0, 0, 0],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0],
]
# From (0, 0) to (0, 2) the shortest route is 2 steps straight right. But
# solve_maze tries up, down, left, right in that order, so it goes down
# first and wanders (0,0) -> (1,0) -> (1,1) -> (0,1) -> (0,2): 4 steps.
DFS_TAKES_THE_LONG_WAY = [
    [0, 0, 0],
    [0, 0, 0],
]


class TestShortestPathLength:
    def test_start_is_end(self):
        assert facit.shortest_path_length(OPEN_GRID, (0, 0), (0, 0)) == 0

    def test_open_grid_corner_to_corner(self):
        assert facit.shortest_path_length(OPEN_GRID, (0, 0), (2, 2)) == 4

    def test_finds_shortest_even_when_dfs_does_not(self):
        dfs_path = solve_maze(DFS_TAKES_THE_LONG_WAY, (0, 0), (0, 2))
        assert len(dfs_path) - 1 == 4
        assert facit.shortest_path_length(DFS_TAKES_THE_LONG_WAY, (0, 0), (0, 2)) == 2

    def test_no_path(self):
        walled = [[0, 1, 0]]
        assert facit.shortest_path_length(walled, (0, 0), (0, 2)) is None

    def test_invalid_start_raises(self):
        with pytest.raises(ValueError):
            facit.shortest_path_length(OPEN_GRID, (5, 5), (0, 0))


class TestNQueens:
    @pytest.mark.parametrize("n", [1, 4, 5, 6, 8])
    def test_solution_is_valid(self, n):
        queens = facit.solve_n_queens(n)
        assert len(queens) == n
        assert len(set(queens)) == n  # one per column
        for r1 in range(n):
            for r2 in range(r1 + 1, n):
                assert abs(queens[r1] - queens[r2]) != r2 - r1  # no shared diagonal

    @pytest.mark.parametrize("n", [2, 3])
    def test_impossible_sizes(self, n):
        assert facit.solve_n_queens(n) is None

    def test_zero_queens_is_the_empty_placement(self):
        assert facit.solve_n_queens(0) == []


class TestAllMazePaths:
    def test_detour_grid_has_two_paths(self):
        paths = facit.all_maze_paths(DETOUR_GRID, (0, 0), (3, 3))
        assert sorted(len(p) for p in paths) == [7, 7]
        assert all(p[0] == (0, 0) and p[-1] == (3, 3) for p in paths)

    def test_paths_never_revisit_a_cell(self):
        for path in facit.all_maze_paths(OPEN_GRID, (0, 0), (2, 2)):
            assert len(path) == len(set(path))

    def test_open_3x3_has_twelve_simple_paths(self):
        assert len(facit.all_maze_paths(OPEN_GRID, (0, 0), (2, 2))) == 12

    def test_no_path_gives_empty_list(self):
        assert facit.all_maze_paths([[0, 1, 0]], (0, 0), (0, 2)) == []


class TestFindSubsetSum:
    def test_returns_a_subset_that_sums_to_target(self):
        subset = facit.find_subset_sum([3, 34, 4, 12, 5, 2], 9)
        assert sum(subset) == 9
        remaining = [3, 34, 4, 12, 5, 2]
        for value in subset:
            remaining.remove(value)  # every chosen value came from the list

    def test_no_subset(self):
        assert facit.find_subset_sum([3, 34, 4, 12, 5, 2], 30) is None

    def test_target_zero_is_the_empty_subset(self):
        assert facit.find_subset_sum([1, 2], 0) == []


class TestPartialPermutations:
    def test_count_and_content_match_itertools(self):
        items = [1, 2, 3, 4]
        result = facit.partial_permutations(items, 2)
        assert len(result) == factorial(4) // factorial(2)
        assert sorted(map(tuple, result)) == sorted(permutations(items, 2))

    def test_k_equal_to_length_gives_full_permutations(self):
        assert len(facit.partial_permutations(["a", "b", "c"], 3)) == 6

    def test_k_zero(self):
        assert facit.partial_permutations([1, 2], 0) == [[]]

    @pytest.mark.parametrize("k", [-1, 3])
    def test_invalid_k(self, k):
        with pytest.raises(ValueError):
            facit.partial_permutations([1, 2], k)
