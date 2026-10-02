"""Tests for the Try It Yourself solutions in facit/prova_sjalv.py."""

import pytest

from diy_data_structures.linked_list import LinkedList
from diy_data_structures.stack import EmptyStackError
from facit import prova_sjalv as facit


def build(cls, values):
    lst = cls()
    for value in values:
        lst.append(value)
    return lst


class TestRepr:
    def test_empty(self):
        assert repr(LinkedList()) == "LinkedList([])"

    def test_values_use_their_own_repr(self):
        assert repr(build(LinkedList, [1, "a", None])) == "LinkedList([1, 'a', None])"


class TestContains:
    def test_in_and_not_in(self):
        lst = build(facit.LinkedListWithContains, ["Oslo", "Umeå"])
        assert "Oslo" in lst
        assert "Kiruna" not in lst

    def test_in_already_worked_through_iter(self):
        # Without __contains__, Python falls back to __iter__ for `in`.
        assert "Oslo" in build(LinkedList, ["Oslo"])


class TestDoublyLinkedList:
    def test_append_prepend_and_both_directions(self):
        lst = facit.DoublyLinkedList()
        lst.append(2)
        lst.append(3)
        lst.prepend(1)
        assert list(lst) == [1, 2, 3]
        assert list(lst.backwards()) == [3, 2, 1]
        assert len(lst) == 3

    @pytest.mark.parametrize("value, expected", [(1, [2, 3]), (2, [1, 3]), (3, [1, 2])])
    def test_delete_head_middle_and_tail_keeps_links_consistent(self, value, expected):
        lst = build(facit.DoublyLinkedList, [1, 2, 3])
        lst.delete(value)
        assert list(lst) == expected
        assert list(lst.backwards()) == expected[::-1]

    def test_delete_only_element(self):
        lst = build(facit.DoublyLinkedList, ["x"])
        lst.delete("x")
        assert lst.head is None and lst.tail is None and len(lst) == 0

    def test_delete_missing_raises(self):
        with pytest.raises(ValueError):
            build(facit.DoublyLinkedList, [1]).delete(9)


class TestDeque:
    def test_both_ends(self):
        d = facit.Deque()
        d.push_back(2)
        d.push_front(1)
        d.push_back(3)
        assert d.pop_back() == 3
        assert d.pop_front() == 1
        assert d.pop_back() == 2
        assert len(d) == 0

    def test_empty_pops_raise(self):
        with pytest.raises(IndexError):
            facit.Deque().pop_back()
        with pytest.raises(IndexError):
            facit.Deque().pop_front()


class TestMinStack:
    def test_min_follows_pushes_and_pops(self):
        s = facit.MinStack()
        s.push(5)
        assert s.get_min() == 5
        s.push(3)
        s.push(7)
        assert s.get_min() == 3
        s.push(1)
        assert s.get_min() == 1
        assert s.pop() == 1
        assert s.get_min() == 3
        assert s.peek() == 7

    def test_duplicates_of_the_minimum(self):
        s = facit.MinStack()
        for value in [2, 2, 2]:
            s.push(value)
        s.pop()
        assert s.get_min() == 2

    def test_empty_get_min_raises(self):
        with pytest.raises(EmptyStackError):
            facit.MinStack().get_min()


class TestReverse:
    def test_reverses_in_place_without_new_nodes(self):
        lst = build(facit.ReversibleLinkedList, [1, 2, 3])
        nodes_before = {id(node) for node in [lst.head, lst.head.next, lst.tail]}
        lst.reverse()
        assert list(lst) == [3, 2, 1]
        assert {id(node) for node in [lst.head, lst.head.next, lst.tail]} == nodes_before

    def test_head_and_tail_swap_so_append_still_works(self):
        lst = build(facit.ReversibleLinkedList, [1, 2, 3])
        lst.reverse()
        assert lst.head.value == 3 and lst.tail.value == 1
        lst.append(0)
        assert list(lst) == [3, 2, 1, 0]

    @pytest.mark.parametrize("values", [[], [1]])
    def test_short_lists(self, values):
        lst = build(facit.ReversibleLinkedList, values)
        lst.reverse()
        assert list(lst) == values
