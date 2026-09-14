import pytest

from diy_data_structures.stack import EmptyStackError, Stack


class TestNormalOperations:
    def test_push_and_pop_are_lifo(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        assert s.pop() == 3
        assert s.pop() == 2
        assert s.pop() == 1

    def test_peek_does_not_remove(self):
        s = Stack()
        s.push(1)
        s.push(2)
        assert s.peek() == 2
        assert len(s) == 2

    def test_len_tracks_pushes_and_pops(self):
        s = Stack()
        assert len(s) == 0
        s.push("a")
        s.push("b")
        assert len(s) == 2
        s.pop()
        assert len(s) == 1

    def test_is_empty(self):
        s = Stack()
        assert s.is_empty() is True
        s.push(1)
        assert s.is_empty() is False


class TestEmptyStackErrors:
    def test_pop_empty_raises(self):
        s = Stack()
        with pytest.raises(EmptyStackError):
            s.pop()

    def test_peek_empty_raises(self):
        s = Stack()
        with pytest.raises(EmptyStackError):
            s.peek()

    def test_pop_after_draining_raises(self):
        s = Stack()
        s.push(1)
        s.pop()
        with pytest.raises(EmptyStackError):
            s.pop()


class TestReuseAfterEmpty:
    def test_stack_usable_after_being_emptied(self):
        s = Stack()
        s.push(1)
        s.pop()
        s.push(2)
        s.push(3)
        assert s.pop() == 3
        assert s.pop() == 2
