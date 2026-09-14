import pytest

from diy_data_structures.queue_ import EmptyQueueError, Queue


class TestNormalOperations:
    def test_enqueue_and_dequeue_are_fifo(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        assert q.dequeue() == 1
        assert q.dequeue() == 2
        assert q.dequeue() == 3

    def test_len_tracks_enqueues_and_dequeues(self):
        q = Queue()
        assert len(q) == 0
        q.enqueue("a")
        q.enqueue("b")
        assert len(q) == 2
        q.dequeue()
        assert len(q) == 1

    def test_is_empty(self):
        q = Queue()
        assert q.is_empty() is True
        q.enqueue(1)
        assert q.is_empty() is False


class TestEmptyQueueErrors:
    def test_dequeue_empty_raises(self):
        q = Queue()
        with pytest.raises(EmptyQueueError):
            q.dequeue()

    def test_dequeue_after_draining_raises(self):
        q = Queue()
        q.enqueue(1)
        q.dequeue()
        with pytest.raises(EmptyQueueError):
            q.dequeue()


class TestReuseAfterEmpty:
    def test_queue_usable_after_being_emptied(self):
        q = Queue()
        q.enqueue(1)
        q.dequeue()
        q.enqueue(2)
        q.enqueue(3)
        assert q.dequeue() == 2
        assert q.dequeue() == 3

    def test_interleaved_enqueue_dequeue(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        assert q.dequeue() == 1
        q.enqueue(3)
        assert q.dequeue() == 2
        assert q.dequeue() == 3
