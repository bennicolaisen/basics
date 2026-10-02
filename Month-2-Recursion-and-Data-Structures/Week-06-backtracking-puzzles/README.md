# Week 6 — Backtracking Puzzles

## Purpose

Week 5 built comfort with recursion where each call does its own
self-contained work (compute a factorial, reverse a string). This week
uses recursion for something different: **searching** through a space of
choices where most paths dead-end, and you need a reliable way to try a
choice, discover it doesn't work, and cleanly go back and try the next
one. That pattern — backtracking — is how you'd solve a maze, deal out
every possible arrangement of a hand of cards, or check whether some
combination of items hits a target weight.

## Objectives

The code in this project demonstrates:

- Generating **every permutation** of a list recursively, with no
  `itertools` — building the "choose one, recurse on the rest, put it
  back" pattern by hand.
- Solving a **maze** with recursive depth-first search, where the
  recursive call stack itself keeps track of the current path.
- Deciding **subset-sum** reachability by explicitly trying "include this
  element" and "exclude this element" as two separate recursive branches.
- Making the **backtrack step itself visible** — every implementation here
  comments on the exact moment a branch is abandoned and why undoing
  matters.

## Concepts Refresher

### Backtracking, defined precisely

Backtracking is **recursion plus an explicit undo when a branch fails**:

1. Make a choice (place a number, step to a neighboring cell, include an
   element).
2. Recurse — explore everything that follows from that choice.
3. If the recursive exploration reports success, propagate that success
   back up immediately.
4. If it reports failure, **undo the choice** you made in step 1 — remove
   it from whatever shared state you built it into — and then try the
   *next* choice at this same level, or report failure upward if there
   are no more choices left to try.

Step 4 is the part that's easy to skip and the whole reason "backtracking"
gets its own name rather than just being "recursion." Skip it, and failed
attempts leave garbage behind in your shared state that corrupts every
later attempt.

### Connecting this to Week 5's call-stack model

Week 5 covered call stack frames — that each call gets a frame holding
its own locals, and frames pop off in the reverse order they were pushed.
Backtracking leans on exactly that property: each recursive call's frame
*is* effectively "the state of the search at this point in the path."
When `maze_solver.py`'s `dfs` calls itself for a neighboring cell and that
call eventually returns `False`, control comes back to the exact point in
the *calling* frame right after that call — which is precisely where the
`path.pop()` undo step lives. You don't need to manually save "what the
path looked like before I tried that neighbor" anywhere, because the call
stack was already keeping it: the parent frame's local view of `path`
picks up again exactly where it left off, only now with the failed
neighbor's entry still sitting on the end of `path`, waiting to be popped.

Without the call stack (e.g. trying to write this iteratively without
building your own explicit stack), you'd have to manage that undo
bookkeeping by hand. That's exactly why backtracking problems are usually
introduced as recursion — the mechanism you need already exists for free.

### Two backtracking shapes used here

- **Include/exclude** (`subset_sum.py`): for each element, there are
  exactly two choices — take it or don't — explored as two separate
  recursive calls. Neither call can affect the other; "undo" here is
  free, because nothing was ever mutated in the first place, so
  "excluding" an element is just calling again with a fresh state that
  never saw it.
- **Explore/retreat over a shared, mutated structure**
  (`maze_solver.py`): here `visited` and `path` *are* mutated as the
  search goes deeper, so undoing is not automatic — `path.pop()` has to
  be written explicitly for the state to go back to how it looked before
  the failed branch was tried. `visited`, by contrast, is deliberately
  *not* undone — see the comment in `maze_solver.py` for why.

## Design & Architecture

```
Week-06-backtracking-puzzles/
├── README.md
├── conftest.py                          # adds src/ to sys.path for pytest
├── src/
│   └── backtracking_puzzles/
│       ├── __init__.py
│       ├── permutations.py              # all_permutations(lst)
│       ├── maze_solver.py               # solve_maze(grid, start, end)
│       └── subset_sum.py                # has_subset_sum(nums, target)
└── tests/
    ├── test_permutations.py
    ├── test_maze_solver.py
    └── test_subset_sum.py
```

Three independent modules, one per puzzle — none of them share code, so
there's no shared base module to introduce. Each file is small enough to
read start to finish in a few minutes.

## How to Build & Run

No build step — pure standard library.

```bash
cd Month-2-Recursion-and-Data-Structures/Week-06-backtracking-puzzles
PYTHONPATH=src python3 -c "
from backtracking_puzzles.maze_solver import solve_maze
grid = [[0, 0, 0], [1, 1, 0], [0, 0, 0]]
print(solve_maze(grid, (0, 0), (2, 2)))
"
```

## Testing

```bash
cd Month-2-Recursion-and-Data-Structures/Week-06-backtracking-puzzles
python -m pytest -q
```

`conftest.py` puts `src/` on `sys.path`, so `pytest` runs with zero
extra flags from this directory. Coverage:

- `permutations.py`: empty list, single element, correct count
  (`n!`) for lists of length 3 and 4, and cross-checked against
  `itertools.permutations` for exact set equality.
- `maze_solver.py`: at least one solvable grid (path validated step by
  step — adjacent cells, all open, correct endpoints) and at least one
  unsolvable grid (returns `None`), plus invalid-input cases (start/end
  out of bounds or on a wall).
- `subset_sum.py`: true and false cases, including the empty-list and
  target-zero edge cases.

## Try It Yourself

> **Facit (answer key):** every exercise below is solved, tested and explained
> in Swedish in [FACIT.md](FACIT.md). Try each one yourself first, then compare.

1. **Return the actual maze path length as a separate function**,
   `shortest_path_length(grid, start, end)`, without changing
   `solve_maze`. (Hint: DFS as written here finds *a* path, not
   necessarily the *shortest* one — is that a problem for this exercise,
   or not? Think about why before changing anything.)
2. **N-Queens.** Write `solve_n_queens(n)` that returns one valid
   placement of `n` queens on an `n x n` board such that none attack each
   other (or `None` if impossible for that `n`), using the same
   choose/recurse/undo shape as `maze_solver.py`.
3. **All maze paths, not just one.** Write `all_maze_paths(grid, start,
   end)` returning *every* valid path from start to end, not just the
   first one DFS finds. What has to change about when you backtrack?
4. **Subset sum with the actual subset.** Write
   `find_subset_sum(nums, target)` that returns the matching subset
   itself (as a list) instead of just `True`/`False`, or `None` if none
   exists.
5. **Permutations of a fixed length.** Write
   `partial_permutations(lst, k)` returning all ordered arrangements of
   exactly `k` elements chosen from `lst` (for `k < len(lst)`), without
   first generating every full permutation and truncating.

## Reflection

`subset_sum`'s include/exclude branches don't need an explicit "undo"
step in code — nothing is mutated, so there's nothing to put back.
`maze_solver`'s `path.pop()` is different: it's undoing a real side
effect on shared state. That distinction matters beyond this week — any
time you reach for backtracking, ask first whether your recursive calls
can work on *independent* copies of state (simpler to reason about, but
copies more memory) or need to *mutate and later undo* shared state
(cheaper, but every mutation needs a matching, correctly-placed undo, or
the search silently corrupts itself).
