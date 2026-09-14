# Week 7 — DIY Data Structures

## Purpose

Python's built-in `list` is so convenient that it's easy to reach for it
for every job without ever having built a data structure yourself — which
means "what's actually a stack, structurally?" or "why is this queue
slow?" can stay fuzzy indefinitely. This week builds a linked list, a
stack, and a queue from nothing but classes and object references, so
those questions have concrete answers instead of vague ones.

## Objectives

The code in this project demonstrates:

- A **singly linked list** built from `Node` objects connected by
  `.next` references — no array underneath at all.
- A **stack** (`push`/`pop`/`peek`, LIFO) and a **queue**
  (`enqueue`/`dequeue`, FIFO), both *composed on top of* that linked list
  rather than reimplemented from scratch or wrapping a Python `list`.
- Custom exceptions (`EmptyStackError`, `EmptyQueueError`) for the one
  case where these structures can genuinely be misused: acting on them
  while empty.
- `__len__` and `__iter__` on every structure, so `len(x)` and
  `for item in x` work the way they would on any built-in container.

## Concepts Refresher

### What a linked list actually is in memory

A Python `list` is (conceptually) one contiguous block of memory holding
references to your elements, side by side, with the list object tracking
where that block starts and how long it is. That's *why* `my_list[500]`
is instant — the address of index 500 is a fixed offset from the start of
the block, no searching required — and why inserting at the front is
expensive: every existing element has to physically shift over by one
slot first.

A linked list has no contiguous block at all. It's a chain of separate
`Node` objects scattered wherever in memory, each one holding a value and
a `.next` reference pointing to the next node (or `None`, marking the
end). The list itself only needs to remember one thing to have the whole
chain: `self.head`, the first node. Getting to element 500 means
following 500 `.next` references one at a time — there's no shortcut,
because there's no fixed offset to jump to. That's the fundamental
trade-off:

| | Python `list` (array) | `LinkedList` here |
|---|---|---|
| Access by index | O(1) | O(n) — must walk from head |
| Insert/delete at the **front** | O(n) — shifts everything | O(1) — just repoint `head` |
| Insert/delete at the **back** | O(1) (amortized) | O(1) **only with a tracked `tail`** |
| Extra memory per element | none | one `.next` reference per node |

`LinkedList` here tracks both `head` and `tail` specifically so that
`append` (add at the back) doesn't have to walk the whole chain just to
find the last node — see `linked_list.py` for exactly where that pointer
gets read and updated.

### Stack and queue are access disciplines, not separate structures

A stack and a queue don't need their own from-scratch node/pointer
machinery — structurally, they're each just a `LinkedList` with a **rule
about where you're allowed to touch it**:

- A **stack** is LIFO (last in, first out): every operation happens at
  one end. `push` and `pop` both act on the head — `Stack.push` calls
  `LinkedList.prepend`, `Stack.pop` reads and removes `LinkedList.head`.
- A **queue** is FIFO (first in, first out): insertion and removal happen
  at *opposite* ends. `enqueue` adds at the tail (`LinkedList.append`),
  `dequeue` removes from the head.

That's the whole idea behind "access discipline": `Stack` and `Queue` in
this project don't know anything about nodes or pointers at all — look at
`stack.py` and `queue_.py` and notice neither one mentions `Node`. They
each hold one `LinkedList` and restrict themselves to calling its
existing methods in a specific pattern. The restriction *is* the data
structure; the nodes-and-pointers machinery underneath is shared,
borrowed, not reimplemented.

### Why `Queue` needs the tail pointer (and `Stack` doesn't)

`Stack.push`/`Stack.pop` only ever touch the head, which `LinkedList`
already tracks directly — no extra bookkeeping needed. `Queue.enqueue`
needs to add at the *tail*, though, and without a tracked `tail` pointer,
finding "the last node" means walking every node in the list each time
— an O(n) `enqueue`, which would make this queue slower than it has any
reason to be. Tracking `tail` (updated in `LinkedList.append` and
`LinkedList.prepend`) is what keeps `enqueue` O(1). `Queue.dequeue`
removes from the head, same as `Stack.pop` — see `LinkedList.delete`'s
docstring for why that's O(1) in practice, not just in theory, even
though `delete` is a general O(n) method.

## Design & Architecture

```
Week-07-diy-data-structures/
├── README.md
├── conftest.py                       # adds src/ to sys.path for pytest
├── src/
│   └── diy_data_structures/
│       ├── __init__.py
│       ├── linked_list.py            # Node, LinkedList — the primitive
│       ├── stack.py                  # Stack + EmptyStackError, built on LinkedList
│       └── queue_.py                 # Queue + EmptyQueueError, built on LinkedList
└── tests/
    ├── test_linked_list.py
    ├── test_stack.py
    └── test_queue.py
```

`linked_list.py` has no dependency on the other two files; `stack.py` and
`queue_.py` both import *only* `LinkedList` from it and nothing from each
other — that one-directional dependency (primitive at the bottom, two
independent structures built on top) is the point of the week, so the
file layout mirrors it directly. (`queue_.py` is spelled with a trailing
underscore only to avoid colliding with Python's own standard-library
`queue` module on `sys.path`.)

## How to Build & Run

No build step — pure standard library.

```bash
cd Month-2-Recursion-and-Data-Structures/Week-07-diy-data-structures
PYTHONPATH=src python3 -c "
from diy_data_structures.stack import Stack
s = Stack()
s.push(1); s.push(2); s.push(3)
print(s.pop(), s.pop(), s.pop())
"
```

## Testing

```bash
cd Month-2-Recursion-and-Data-Structures/Week-07-diy-data-structures
python -m pytest -q
```

`conftest.py` puts `src/` on `sys.path`, so `pytest` runs with zero extra
flags from this directory. Coverage:

- `LinkedList`: `append`/`prepend` (including head/tail pointer
  correctness), `delete` (head, middle, tail, only-element, and
  not-found), `find`, `__len__`, and `__iter__` (including iterating an
  empty list).
- `Stack`: LIFO ordering, `peek` vs `pop`, `is_empty`, `__len__`, and that
  both `pop` and `peek` raise `EmptyStackError` on an empty stack —
  including reuse after the stack has been drained once.
- `Queue`: FIFO ordering, `is_empty`, `__len__`, `EmptyQueueError` on an
  empty `dequeue`, interleaved enqueue/dequeue sequences, and reuse after
  being drained.

## Try It Yourself

1. **`__repr__` isn't tested here — write tests for it.** Then add a
   `__contains__` to `LinkedList` so `value in my_list` works without
   calling `.find(...)` explicitly, and test that too.
2. **A doubly linked list.** Add a `.prev` reference to `Node` (or a new
   `DoublyLinkedList`) and implement `append`/`prepend`/`delete` for it.
   What operation that's O(n) in the singly linked version becomes O(1)
   with a `.prev` pointer?
3. **`Deque` (double-ended queue).** Build a structure supporting
   `push_front`, `push_back`, `pop_front`, `pop_back`, all O(1) — you'll
   need the doubly linked list from exercise 2, or a very careful singly
   linked design. Explain in a comment why a *singly* linked list can't
   give you `pop_back` in O(1) no matter how it's arranged.
4. **A `MinStack`.** Build a stack with an added `get_min()` operation
   that returns the current minimum element in O(1) — no scanning the
   whole stack when asked. (Hint: what if every node carried a little
   extra information alongside its value?)
5. **Reverse a `LinkedList` in place.** Write `LinkedList.reverse()`,
   which flips the direction of every `.next` pointer so the list reads
   backwards, *without* creating any new `Node` objects — only
   re-pointing existing ones. Watch out for `head`/`tail` needing to
   swap too.

## Reflection

`LinkedList.delete(value)` is a general-purpose, by-value O(n) removal —
but `Stack.pop` and `Queue.dequeue` both get away with treating it as
O(1). That's not a coincidence baked into `delete`'s implementation by
accident: both callers only ever pass `self._list.head.value`, so the
very first comparison inside `delete`'s scan is always the match. That's
a useful thing to notice generally — a function's *worst-case* complexity
and the complexity you actually get *at a specific call site* can be very
different, depending on what that call site guarantees about its own
inputs. It's also a bit fragile: nothing about `Stack`/`Queue`'s method
signatures documents that guarantee anywhere `delete` itself can see it,
which is a real cost of building `Stack`/`Queue` on a shared, more
general primitive rather than giving them their own dedicated
`remove_head()` — a trade-off worth naming rather than treating as free.
