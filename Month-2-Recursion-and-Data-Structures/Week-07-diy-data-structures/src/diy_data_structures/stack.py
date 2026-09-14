"""A LIFO stack, composed on top of `LinkedList` rather than wrapping a
Python `list`. This is an *access discipline* layered on the linked list:
`Stack` doesn't reimplement node/pointer logic at all, it just restricts
where `LinkedList` is touched — always at the head.
"""

from diy_data_structures.linked_list import LinkedList


class EmptyStackError(Exception):
    """Raised by pop()/peek() when the stack has no elements."""


class Stack:
    def __init__(self):
        self._list = LinkedList()

    def push(self, value) -> None:
        """Add value to the top of the stack. O(1): prepend is a head
        insertion, same operation LinkedList already does in O(1)."""
        self._list.prepend(value)

    def pop(self):
        """Remove and return the top value. O(1): the top is always the
        list's head, so delete()'s first comparison is the match."""
        if self.is_empty():
            raise EmptyStackError("pop from an empty stack")
        value = self._list.head.value
        self._list.delete(value)
        return value

    def peek(self):
        """Return the top value without removing it."""
        if self.is_empty():
            raise EmptyStackError("peek at an empty stack")
        return self._list.head.value

    def is_empty(self) -> bool:
        return len(self._list) == 0

    def __len__(self) -> int:
        return len(self._list)
