"""Tests for the number guessing game."""

import unittest

from main import main, play_game


class FixedRandom:
    """Small random-number stand-in that always chooses a known value."""

    def __init__(self, number):
        self.number = number

    def randint(self, lower, upper):
        return self.number


class NumberGuessingGameTests(unittest.TestCase):
    def test_higher_and_lower_hints_then_win(self):
        guesses = iter(["25", "75", "50"])
        messages = []
        play_game(lambda _prompt: next(guesses), messages.append, FixedRandom(50))
        self.assertTrue(any("higher" in message for message in messages))
        self.assertTrue(any("lower" in message for message in messages))
        self.assertTrue(any("Correct!" in message for message in messages))

    def test_invalid_inputs_do_not_consume_attempts(self):
        guesses = iter(["hello", "0", "42"])
        messages = []
        play_game(lambda _prompt: next(guesses), messages.append, FixedRandom(42))
        self.assertTrue(any("whole number" in message for message in messages))
        self.assertTrue(any("between 1 and 100" in message for message in messages))
        self.assertTrue(any("Correct!" in message for message in messages))

    def test_limited_attempts_end_round(self):
        guesses = iter(["1"] * 7)
        messages = []
        play_game(lambda _prompt: next(guesses), messages.append, FixedRandom(100))
        self.assertTrue(any("Out of attempts" in message for message in messages))

    def test_replay_and_replay_input_validation(self):
        answers = iter(["50", "maybe", "yes", "50", "no"])
        messages = []
        main(lambda _prompt: next(answers), messages.append, FixedRandom(50))
        self.assertEqual(sum("Correct!" in message for message in messages), 2)
        self.assertTrue(any("Please answer yes or no" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
