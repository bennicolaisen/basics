"""A singly linked list built from nothing but `Node` objects and pointers
— no `collections.deque`, no wrapping a Python `list` internally. This is
the primitive structure `Stack` and `Queue` in this same project are built
on top of.
"""


class Node:
    """One link in the chain: a value, plus a reference to the next Node
    (or None, if this is the last node)."""

    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    """A singly linked list with a tracked head *and* tail pointer.

    Tracking `tail` (not just `head`) is what makes `append` O(1) instead
    of O(n) — without it, adding to the end would require walking the
    whole list every time to find the last node.
    """

    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self._size = 0

    def append(self, value) -> None:
        """Add value as the new last element. O(1): the tail pointer
        means there's no need to walk the list to find the end."""
        node = Node(value)
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def prepend(self, value) -> None:
        """Add value as the new first element. O(1): a new head just
        points at the old head, no walking required."""
        node = Node(value)
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = node
        self._size += 1

    def delete(self, value) -> None:
        """Remove the first node whose value equals `value`.

        O(n) in general (may need to scan the whole list) — but O(1) in
        the specific, common case where the matching node is the head,
        since the very first comparison already finds it. `Stack.pop` and
        `Queue.dequeue` in this project rely on exactly that case.

        Raises ValueError if value isn't found — mirrors `list.remove`.
        """
        prev = None
        node = self.head
        while node is not None:
            if node.value == value:
                if prev is None:
                    self.head = node.next
                else:
                    prev.next = node.next
                if node is self.tail:
                    self.tail = prev
                self._size -= 1
                return
            prev = node
            node = node.next
        raise ValueError(f"{value!r} not found in list")

    def find(self, value) -> bool:
        """Return True if value appears anywhere in the list. O(n)."""
        for item in self:
            if item == value:
                return True
        return False

    def to_list(self) -> list:
        """Return a plain Python list of the values, head to tail."""
        return list(self)

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def __repr__(self) -> str:
        return f"LinkedList({self.to_list()!r})"
