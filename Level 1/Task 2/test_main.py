"""Unit tests for number patterns and interactive input validation."""

import unittest

from main import (
    decreasing_triangle,
    floyd_triangle,
    increasing_triangle,
    main,
    number_pyramid,
)


class PatternTests(unittest.TestCase):
    def test_increasing_triangle(self):
        self.assertEqual(increasing_triangle(3), ["1", "1 2", "1 2 3"])

    def test_decreasing_triangle(self):
        self.assertEqual(decreasing_triangle(3), ["1 2 3", "1 2", "1"])

    def test_number_pyramid(self):
        result = number_pyramid(3)
        self.assertEqual(len(result), 3)
        self.assertEqual([line.strip() for line in result], ["1", "2 2", "3 3 3"])
        self.assertGreater(len(result[0]) - len(result[0].lstrip()), len(result[1]) - len(result[1].lstrip()))
        self.assertGreater(len(result[1]) - len(result[1].lstrip()), len(result[2]) - len(result[2].lstrip()))

    def test_floyd_triangle(self):
        self.assertEqual(floyd_triangle(3), ["1", "2 3", "4 5 6"])

    def test_patterns_reject_invalid_rows(self):
        for pattern in (increasing_triangle, decreasing_triangle, number_pyramid, floyd_triangle):
            for rows in (0, -1, 1.5, True):
                with self.subTest(pattern=pattern.__name__, rows=rows):
                    with self.assertRaises(ValueError):
                        pattern(rows)


class InputValidationTests(unittest.TestCase):
    def test_invalid_pattern_choice(self):
        inputs = iter(["9"])
        output = []
        main(lambda _prompt: next(inputs), output.append)
        self.assertTrue(any("Invalid pattern choice" in line for line in output))

    def test_invalid_row_count(self):
        for raw_rows in ("abc", "0", "-2", "2.5"):
            with self.subTest(rows=raw_rows):
                inputs = iter(["1", raw_rows])
                output = []
                main(lambda _prompt: next(inputs), output.append)
                self.assertTrue(any("positive whole number" in line for line in output))

    def test_valid_selection_prints_pattern(self):
        inputs = iter(["4", "3"])
        output = []
        main(lambda _prompt: next(inputs), output.append)
        self.assertIn("1", output)
        self.assertIn("2 3", output)
        self.assertIn("4 5 6", output)


if __name__ == "__main__":
    unittest.main()
