"""Regression checks: malformed parity inputs must not yield zero discrepancy."""

import math
import unittest

from analysis.make_outputs import abs_max, rel_max


class TestParityOracleShapeAndFiniteness(unittest.TestCase):
    def test_identical_numeric_arrays_pass(self):
        self.assertEqual(rel_max([0.1, 2.0], [0.1, 2.0]), 0.0)
        self.assertEqual(abs_max([-0.2, 0.5], [-0.2, 0.5]), 0.0)

    def test_valid_discrepancy_unchanged(self):
        self.assertAlmostEqual(rel_max([1.3, 0.5], [1.0, 0.5]), 0.3)
        self.assertAlmostEqual(abs_max([1.3, 0.5], [1.0, 0.5]), 0.3)

    def test_missing_trailing_result_rejected(self):
        for fun in (rel_max, abs_max):
            with self.subTest(function=fun.__name__):
                with self.assertRaises(ValueError):
                    fun([0.1], [0.1, 0.9])

    def test_extra_app_result_rejected(self):
        for fun in (rel_max, abs_max):
            with self.subTest(function=fun.__name__):
                with self.assertRaises(ValueError):
                    fun([0.1, 0.9], [0.1])

    def test_empty_arrays_rejected(self):
        for fun in (rel_max, abs_max):
            with self.subTest(function=fun.__name__):
                with self.assertRaises(ValueError):
                    fun([], [])

    def test_nan_any_position_rejected(self):
        for fun in (rel_max, abs_max):
            for candidate in ([math.nan, 0.0], [0.0, math.nan]):
                with self.assertRaises(ValueError):
                    fun(candidate, [0.0, 1.0])

    def test_inf_any_position_rejected(self):
        for fun in (rel_max, abs_max):
            with self.assertRaises(ValueError):
                fun([0.0, math.inf], [0.0, 1.0])

    def test_nonnumeric_values_rejected(self):
        for fun in (rel_max, abs_max):
            for value in (None, "not-a-number", True):
                with self.assertRaises(ValueError):
                    fun([0.0, value], [0.0, 1.0])


if __name__ == "__main__":
    unittest.main()
