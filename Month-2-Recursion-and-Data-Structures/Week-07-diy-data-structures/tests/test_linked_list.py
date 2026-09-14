import pytest

from diy_data_structures.linked_list import LinkedList


class TestAppendAndPrepend:
    def test_append_builds_order(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        assert ll.to_list() == [1, 2, 3]

    def test_prepend_builds_reverse_order(self):
        ll = LinkedList()
        ll.prepend(1)
        ll.prepend(2)
        ll.prepend(3)
        assert ll.to_list() == [3, 2, 1]

    def test_mixed_append_prepend(self):
        ll = LinkedList()
        ll.append(2)
        ll.prepend(1)
        ll.append(3)
        assert ll.to_list() == [1, 2, 3]

    def test_tail_updated_after_append(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        assert ll.tail.value == 2

    def test_head_and_tail_same_node_for_single_element(self):
        ll = LinkedList()
        ll.append(42)
        assert ll.head is ll.tail
        assert ll.head.value == 42


class TestLen:
    def test_empty_list_len_zero(self):
        assert len(LinkedList()) == 0

    def test_len_tracks_insertions(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.prepend(0)
        assert len(ll) == 3


class TestFind:
    def test_find_present(self):
        ll = LinkedList()
        ll.append("a")
        ll.append("b")
        assert ll.find("b") is True

    def test_find_absent(self):
        ll = LinkedList()
        ll.append("a")
        assert ll.find("z") is False

    def test_find_on_empty_list(self):
        assert LinkedList().find(1) is False


class TestDelete:
    def test_delete_head(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.delete(1)
        assert ll.to_list() == [2, 3]
        assert ll.head.value == 2

    def test_delete_tail_updates_tail_pointer(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.delete(3)
        assert ll.to_list() == [1, 2]
        assert ll.tail.value == 2

    def test_delete_middle(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.delete(2)
        assert ll.to_list() == [1, 3]

    def test_delete_only_element_empties_head_and_tail(self):
        ll = LinkedList()
        ll.append(1)
        ll.delete(1)
        assert ll.head is None
        assert ll.tail is None
        assert len(ll) == 0

    def test_delete_missing_value_raises(self):
        ll = LinkedList()
        ll.append(1)
        with pytest.raises(ValueError):
            ll.delete(99)

    def test_delete_first_of_duplicates_only(self):
        ll = LinkedList()
        ll.append(5)
        ll.append(5)
        ll.delete(5)
        assert len(ll) == 1


class TestIteration:
    def test_for_loop_over_list(self):
        ll = LinkedList()
        ll.append("x")
        ll.append("y")
        ll.append("z")
        collected = [item for item in ll]
        assert collected == ["x", "y", "z"]

    def test_iterate_empty_list(self):
        assert list(LinkedList()) == []

    def test_len_matches_iteration_count(self):
        ll = LinkedList()
        for value in range(5):
            ll.append(value)
        assert sum(1 for _ in ll) == len(ll)
