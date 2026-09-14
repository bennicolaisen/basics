"""A FIFO queue, composed on top of `LinkedList` rather than wrapping a
Python `list` (a `list.pop(0)` would be O(n) — see the README's Design &
Architecture for why that matters). Like `Stack`, this is an access
discipline layered on the same underlying linked list: `Queue` always
adds at the tail and removes at the head.

Named `queue_.py` (trailing underscore) only to avoid shadowing the
standard library's `queue` module on `sys.path`.
"""

from diy_data_structures.linked_list import LinkedList


class EmptyQueueError(Exception):
    """Raised by dequeue() when the queue has no elements."""


class Queue:
    def __init__(self):
        self._list = LinkedList()

    def enqueue(self, value) -> None:
        """Add value to the back of the queue. O(1): LinkedList tracks a
        tail pointer, so append() never has to walk the list to find the
        end — without that tail pointer, this would degrade to O(n)."""
        self._list.append(value)

    def dequeue(self):
        """Remove and return the value at the front of the queue. O(1):
        the front is always the list's head, so delete()'s first
        comparison is the match."""
        if self.is_empty():
            raise EmptyQueueError("dequeue from an empty queue")
        value = self._list.head.value
        self._list.delete(value)
        return value

    def is_empty(self) -> bool:
        return len(self._list) == 0

    def __len__(self) -> int:
        return len(self._list)
