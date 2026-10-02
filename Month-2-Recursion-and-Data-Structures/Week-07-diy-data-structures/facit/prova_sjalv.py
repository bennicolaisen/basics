"""Facit till "Try It Yourself" i vecka 7. Förklaringarna finns i FACIT.md.

Lösningarna bygger vidare på veckans klasser med arv, så att
referenskoden står kvar orörd. I ett riktigt projekt skulle metoderna i
uppgift 1 och 5 läggas direkt i LinkedList.
"""

from diy_data_structures.linked_list import LinkedList
from diy_data_structures.stack import EmptyStackError, Stack


# Uppgift 1: __contains__ (testerna för __repr__ finns i tests/test_facit.py).
class LinkedListWithContains(LinkedList):
    def __contains__(self, value) -> bool:
        return self.find(value)


# Uppgift 2: dubbellänkad lista.
class DoublyNode:
    def __init__(self, value):
        self.value = value
        self.prev: DoublyNode | None = None
        self.next: DoublyNode | None = None


class DoublyLinkedList:
    def __init__(self):
        self.head: DoublyNode | None = None
        self.tail: DoublyNode | None = None
        self._size = 0

    def append(self, value) -> None:
        node = DoublyNode(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1

    def prepend(self, value) -> None:
        node = DoublyNode(value)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._size += 1

    def _unlink(self, node: DoublyNode) -> None:
        """Ta bort en nod man redan har i handen. O(1): båda grannarna nås direkt."""
        if node.prev is None:
            self.head = node.next
        else:
            node.prev.next = node.next
        if node.next is None:
            self.tail = node.prev
        else:
            node.next.prev = node.prev
        self._size -= 1

    def delete(self, value) -> None:
        """Ta bort den första noden med value. O(n) för att hitta den, O(1) för att ta bort den."""
        node = self.head
        while node is not None:
            if node.value == value:
                self._unlink(node)
                return
            node = node.next
        raise ValueError(f"{value!r} not found in list")

    def pop_back(self):
        """Ta bort och returnera det sista värdet. O(1) tack vare tail.prev."""
        if self.tail is None:
            raise IndexError("pop from an empty list")
        value = self.tail.value
        self._unlink(self.tail)
        return value

    def pop_front(self):
        if self.head is None:
            raise IndexError("pop from an empty list")
        value = self.head.value
        self._unlink(self.head)
        return value

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def backwards(self):
        node = self.tail
        while node is not None:
            yield node.value
            node = node.prev


# Uppgift 3: en deque ovanpå den dubbellänkade listan.
class Deque:
    """Kö med två ändar: alla fyra operationerna är O(1).

    Med en enkellänkad lista går pop_back inte att göra i O(1), hur man än
    ordnar den: för att ta bort den sista noden måste man ändra den
    näst sista nodens next till None, och den näst sista går bara att nå
    genom att gå igenom listan från början. En pekare till den näst sista
    hjälper inte heller, för efter borttagningen behövs i sin tur den
    tredje sista, och så vidare. Det som behövs är en pekare bakåt från
    varje nod, och det är precis vad en dubbellänkad lista har.
    """

    def __init__(self):
        self._list = DoublyLinkedList()

    def push_front(self, value) -> None:
        self._list.prepend(value)

    def push_back(self, value) -> None:
        self._list.append(value)

    def pop_front(self):
        return self._list.pop_front()

    def pop_back(self):
        return self._list.pop_back()

    def __len__(self) -> int:
        return len(self._list)


# Uppgift 4: en stack som vet sitt minsta värde i O(1).
class MinStack:
    """Varje element sparas tillsammans med det minsta värdet i stacken när det lades dit."""

    def __init__(self):
        self._stack = Stack()

    def push(self, value) -> None:
        if self._stack.is_empty():
            smallest = value
        else:
            smallest = min(value, self._stack.peek()[1])
        self._stack.push((value, smallest))

    def pop(self):
        value, _ = self._stack.pop()
        return value

    def peek(self):
        return self._stack.peek()[0]

    def get_min(self):
        if self._stack.is_empty():
            raise EmptyStackError("get_min on an empty stack")
        return self._stack.peek()[1]

    def __len__(self) -> int:
        return len(self._stack)


# Uppgift 5: vänd en lista utan att skapa nya noder.
class ReversibleLinkedList(LinkedList):
    def reverse(self) -> None:
        previous = None
        node = self.head
        self.tail = self.head          # den gamla första noden blir den nya sista
        while node is not None:
            following = node.next      # spara vägen vidare innan pekaren vänds
            node.next = previous       # vänd pekaren
            previous = node
            node = following
        self.head = previous           # den gamla sista noden blir den nya första
