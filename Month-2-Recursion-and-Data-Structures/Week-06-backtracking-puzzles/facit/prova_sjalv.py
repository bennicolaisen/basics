"""Facit till "Try It Yourself" i vecka 6. Förklaringarna finns i FACIT.md."""

from collections import deque

Coord = tuple[int, int]

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def _in_bounds(grid: list[list[int]], cell: Coord) -> bool:
    row, col = cell
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def _is_open(grid: list[list[int]], cell: Coord) -> bool:
    return _in_bounds(grid, cell) and grid[cell[0]][cell[1]] == 0


def _validate(grid: list[list[int]], start: Coord, end: Coord) -> None:
    """Samma kontroller som solve_maze gör av start och slut."""
    for name, cell in (("start", start), ("end", end)):
        if not _in_bounds(grid, cell):
            raise ValueError(f"{name} {cell} is outside the grid")
        if not _is_open(grid, cell):
            raise ValueError(f"{name} {cell} is a wall")


# Uppgift 1: kortaste vägen kräver bredden-först-sökning, inte djupet-först.
def shortest_path_length(grid: list[list[int]], start: Coord, end: Coord) -> int | None:
    """Antalet steg på den kortaste vägen från start till end, eller None om ingen väg finns."""
    _validate(grid, start, end)
    distance = {start: 0}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        if cell == end:
            return distance[cell]
        for d_row, d_col in MOVES:
            neighbor = (cell[0] + d_row, cell[1] + d_col)
            if _is_open(grid, neighbor) and neighbor not in distance:
                distance[neighbor] = distance[cell] + 1
                queue.append(neighbor)
    return None


# Uppgift 2
def solve_n_queens(n: int) -> list[int] | None:
    """En placering av n damer, som en lista där index är rad och värdet kolumn, eller None."""
    if n < 0:
        raise ValueError(f"n must be >= 0, got {n}")
    queens: list[int] = []

    def is_safe(col: int) -> bool:
        row = len(queens)
        for other_row, other_col in enumerate(queens):
            same_column = other_col == col
            same_diagonal = abs(other_col - col) == row - other_row
            if same_column or same_diagonal:
                return False
        return True

    def place(row: int) -> bool:
        if row == n:
            return True
        for col in range(n):
            if is_safe(col):
                queens.append(col)        # välj
                if place(row + 1):        # gå vidare
                    return True
                queens.pop()              # ångra
        return False

    if place(0):
        return list(queens)
    return None


# Uppgift 3
def all_maze_paths(grid: list[list[int]], start: Coord, end: Coord) -> list[list[Coord]]:
    """Alla vägar från start till end som inte besöker samma ruta två gånger."""
    _validate(grid, start, end)
    paths: list[list[Coord]] = []
    path: list[Coord] = []
    on_path: set[Coord] = set()

    def explore(cell: Coord) -> None:
        if not _is_open(grid, cell) or cell in on_path:
            return
        path.append(cell)
        on_path.add(cell)
        if cell == end:
            paths.append(list(path))
        else:
            for d_row, d_col in MOVES:
                explore((cell[0] + d_row, cell[1] + d_col))
        # Ångra helt, även markeringen: rutan får användas av andra vägar.
        path.pop()
        on_path.remove(cell)

    explore(start)
    return paths


# Uppgift 4
def find_subset_sum(nums: list[float], target: float) -> list[float] | None:
    """En delmängd av nums vars summa är target, eller None om ingen finns."""
    chosen: list[float] = []

    def backtrack(index: int, remaining: float) -> bool:
        if remaining == 0:
            return True
        if index >= len(nums):
            return False
        chosen.append(nums[index])                       # pröva att ta med talet
        if backtrack(index + 1, remaining - nums[index]):
            return True
        chosen.pop()                                     # ångra
        return backtrack(index + 1, remaining)           # pröva utan talet

    if backtrack(0, target):
        return list(chosen)
    return None


# Uppgift 5
def partial_permutations(lst: list, k: int) -> list[list]:
    """Alla ordnade urval av k element ur lst."""
    if k < 0 or k > len(lst):
        raise ValueError(f"k must be between 0 and {len(lst)}, got {k}")
    if k == 0:
        return [[]]
    result = []
    for i in range(len(lst)):
        rest = lst[:i] + lst[i + 1:]
        for tail in partial_permutations(rest, k - 1):
            result.append([lst[i]] + tail)
    return result
