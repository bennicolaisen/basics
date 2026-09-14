"""Solve a maze with recursive depth-first search and backtracking.

The maze is a 2D list of ints: 0 means open, 1 means wall. `solve_maze`
returns the sequence of (row, col) coordinates from start to end, or None
if no path exists.
"""

Coord = tuple[int, int]

_MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right


def solve_maze(grid: list[list[int]], start: Coord, end: Coord) -> list[Coord] | None:
    """Find an open path from start to end in grid via recursive DFS.

    Raises ValueError if start or end is out of bounds or sits on a wall
    (those are invalid inputs, not "no path exists" cases).
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    def in_bounds(coord: Coord) -> bool:
        r, c = coord
        return 0 <= r < rows and 0 <= c < cols

    def is_open(coord: Coord) -> bool:
        r, c = coord
        return grid[r][c] == 0

    for name, coord in (("start", start), ("end", end)):
        if not in_bounds(coord):
            raise ValueError(f"{name} {coord} is outside the grid")
        if not is_open(coord):
            raise ValueError(f"{name} {coord} is a wall")

    visited: set[Coord] = set()
    path: list[Coord] = []

    def dfs(cell: Coord) -> bool:
        if not in_bounds(cell) or not is_open(cell) or cell in visited:
            return False

        visited.add(cell)
        path.append(cell)

        if cell == end:
            return True

        r, c = cell
        for dr, dc in _MOVES:
            if dfs((r + dr, c + dc)):
                return True

        # Backtrack: every neighbor of `cell` led to a dead end, so `cell`
        # itself is not part of a solution — undo adding it to the path
        # before returning control to the caller that placed it. Without
        # this pop(), a dead-end cell would stay stuck in `path` forever,
        # and the final path would include cells that don't actually lead
        # anywhere. `visited` deliberately keeps the cell marked, so DFS
        # never wastes time re-exploring a dead end from another neighbor.
        path.pop()
        return False

    if dfs(start):
        return path
    return None
