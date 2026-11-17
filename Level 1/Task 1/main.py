"""A beginner-friendly number guessing game."""

import random


def play_game(input_fn=input, print_fn=print, rng=random):
    """Play one round; invalid guesses do not use an attempt."""
    secret_number = rng.randint(1, 100)
    attempts_left = 7
    print_fn("I'm thinking of a number from 1 to 100.")

    while attempts_left > 0:
        raw_guess = input_fn(f"Enter your guess ({attempts_left} attempts left): ").strip()

        # Validate the text before converting it to an integer.
        if not raw_guess.isdigit():
            print_fn("Please enter a whole number between 1 and 100.")
            continue

        guess = int(raw_guess)
        if not 1 <= guess <= 100:
            print_fn("Your guess must be between 1 and 100.")
            continue

        attempts_left -= 1
        if guess == secret_number:
            print_fn(f"Correct! You guessed it in {7 - attempts_left} attempt(s).")
            return
        if guess < secret_number:
            print_fn("Too low! Try a higher number.")
        else:
            print_fn("Too high! Try a lower number.")

    print_fn(f"Out of attempts! The number was {secret_number}.")


def main(input_fn=input, print_fn=print, rng=random):
    """Run rounds until the player chooses not to replay."""
    while True:
        play_game(input_fn, print_fn, rng)
        while True:
            replay = input_fn("Would you like to play again? (yes/no): ").strip().lower()
            if replay in ("yes", "y"):
                break
            if replay in ("no", "n"):
                print_fn("Thanks for playing!")
                return
            print_fn("Please answer yes or no.")


if __name__ == "__main__":
    main()
