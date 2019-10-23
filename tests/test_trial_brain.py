import unittest

from brains.trial import (
    SquareGrid,
    PriorityQueue,
    heuristic
)


class SquareGridTestes(unittest.TestCase):

    def test_in_bound_with_valid_location(self):
        grid = SquareGrid(5, 5)
        loc = (2, 2)
        self.assertTrue(grid.in_bounds(loc))

    def test_in_bound_with_invalid_x(self):
        grid = SquareGrid(5, 5)
        loc = (8, 2)
        self.assertFalse(grid.in_bounds(loc))

    def test_in_bound_with_invalid_y(self):
        grid = SquareGrid(5, 5)
        loc = (2, 8)
        self.assertFalse(grid.in_bounds(loc))

    def test_in_bound_with_invalid_loc(self):
        grid = SquareGrid(5, 5)
        loc = (8, 8)
        self.assertFalse(grid.in_bounds(loc))

    def test_is_not_passable_for_location_that_is_a_wall(self):
        grid = SquareGrid(5, 5)
        grid.walls = [(2, 2)]
        loc = (2, 2)
        self.assertFalse(grid.passable(loc))

    def test_is_passable_for_location_that_is_not_a_wall(self):
        grid = SquareGrid(5, 5)
        grid.walls = [(2, 2)]
        loc = (3, 3)
        self.assertTrue(grid.passable(loc))

    def test_neighbors_are_all_passable_and_inbounds(self):
        grid = SquareGrid(5, 5)
        loc = (2, 2)
        expected = [(2, 3), (1, 2), (2, 1), (3, 2)]
        self.assertEqual(grid.neighbors(loc), expected)

    def test_neighbors_removes_unpassable_squares(self):
        grid = SquareGrid(5, 5)
        grid.walls = [(1, 2), (3, 2)]
        loc = (2, 2)
        expected = [(2, 3), (2, 1)]
        self.assertEqual(grid.neighbors(loc), expected)

    def test_neighbors_removes_out_of_bounds(self):
        grid = SquareGrid(5, 5)
        loc = (0, 2)
        expected = [(0, 3), (0, 1), (1, 2)]
        self.assertEqual(grid.neighbors(loc), expected)


class PriorityQueueTests(unittest.TestCase):

    def test_empty_if_no_elements(self):
        q = PriorityQueue()
        self.assertTrue(q.empty)

    def test_empty_is_false_if_elements(self):
        q = PriorityQueue()
        q.elements = ['a']
        self.assertFalse(q.empty)

    def test_put_adds_items_to_elements(self):
        q = PriorityQueue()
        q.put('a', 1)
        self.assertEqual(q.elements, [(1, 'a')])

    def test_get_returns_lowest_priority_item(self):
        q = PriorityQueue()
        q.put('a', 9)
        q.put('b', 1)
        q.put('c', 5)
        self.assertEqual(q.get(), 'b')
        self.assertEqual(q.get(), 'c')
        self.assertEqual(q.get(), 'a')


class HeuristicTest(unittest.TestCase):

    def test_heuristic_with_positive_numbers(self):
        a = (10, 10)
        b = (5, 5)
        result = heuristic(a, b)
        self.assertEqual(result, 10)

    def test_heuristic_with_negative_numbers(self):
        a = (-10, -10)
        b = (5, 5)
        result = heuristic(a, b)
        self.assertEqual(result, 30)
