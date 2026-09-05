"""Unit tests for the Day 22 theme park queue simulator."""

import pytest

from day22_Theme_Park_FastPass_Simulator import ThemeParkQueue


def test_vip_visitors_are_served_first_and_fifo_within_each_lane():
    queue = ThemeParkQueue()
    queue.enqueue("normal-1")
    queue.enqueue("vip-1", vip=True)
    queue.enqueue("normal-2")
    queue.enqueue("vip-2", vip=True)

    assert [visitor.name for visitor in queue.process_all()] == [
        "vip-1",
        "vip-2",
        "normal-1",
        "normal-2",
    ]


def test_snapshot_shows_waiting_visitors_by_lane():
    queue = ThemeParkQueue()
    queue.enqueue("Maya")
    queue.enqueue("Leo", vip=True)

    assert queue.snapshot() == {"vip": ["Leo"], "normal": ["Maya"]}


def test_process_next_returns_none_when_empty():
    queue = ThemeParkQueue()

    assert queue.process_next() is None
    assert "queue empty" in queue.visualize()


def test_visualize_records_each_operation_in_order():
    queue = ThemeParkQueue()
    queue.enqueue("Maya")
    queue.enqueue("Leo", vip=True)
    queue.process_next()

    timeline = queue.visualize()
    assert "1. JOIN  NORMAL Maya" in timeline
    assert "2. JOIN  VIP    Leo" in timeline
    assert "3. SERVE VIP    Leo" in timeline


def test_rejects_blank_visitor_names():
    with pytest.raises(ValueError, match="name cannot be empty"):
        ThemeParkQueue().enqueue("   ")