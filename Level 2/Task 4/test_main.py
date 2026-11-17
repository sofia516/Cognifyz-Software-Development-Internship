"""Unit tests for conversion functions and menu input handling."""

import unittest

from main import celsius_to_fahrenheit, fahrenheit_to_celsius, run_menu


class ConversionTests(unittest.TestCase):
    def test_celsius_to_fahrenheit_zero_negative_and_decimal(self):
        self.assertEqual(celsius_to_fahrenheit(0), 32)
        self.assertEqual(celsius_to_fahrenheit(-40), -40)
        self.assertAlmostEqual(celsius_to_fahrenheit(21.5), 70.7)

    def test_fahrenheit_to_celsius_zero_negative_and_decimal(self):
        self.assertAlmostEqual(fahrenheit_to_celsius(32), 0)
        self.assertAlmostEqual(fahrenheit_to_celsius(-40), -40)
        self.assertAlmostEqual(fahrenheit_to_celsius(70.7), 21.5)


class MenuTests(unittest.TestCase):
    def test_repeated_conversions_format_to_two_decimals(self):
        answers = iter(["1", "0", "2", "32", "3"])
        output = []
        run_menu(lambda _prompt: next(answers), output.append)
        self.assertIn("0 °C = 32.00 °F", output)
        self.assertIn("32 °F = 0.00 °C", output)

    def test_invalid_menu_choice_is_handled(self):
        answers = iter(["x", "3"])
        output = []
        run_menu(lambda _prompt: next(answers), output.append)
        self.assertTrue(any("Invalid menu choice" in line for line in output))

    def test_invalid_temperature_is_handled_and_menu_continues(self):
        for invalid in ("abc", "", "NaN", "inf"):
            with self.subTest(value=invalid):
                answers = iter(["1", invalid, "3"])
                output = []
                run_menu(lambda _prompt: next(answers), output.append)
                self.assertTrue(any("numeric temperature" in line or "finite numeric" in line for line in output))
                self.assertIn("Goodbye!", output)


if __name__ == "__main__":
    unittest.main()
