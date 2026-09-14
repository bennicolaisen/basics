"""A number-guessing CLI game built on top of `parse_int_in_range`.

The game's control flow (a `while` loop bounded by a max-attempt counter,
with `break` on a win) is the actual teaching point this week — the
validator is reused rather than reimplemented here, showing that once a
piece of logic is a tested function, other code just calls it.
"""

import random

from validators_and_games.validators import parse_int_in_range

DEFAULT_LOW = 1
DEFAULT_HIGH = 100
DEFAULT_MAX_ATTEMPTS = 7


def prompt_guess(lo: int, hi: int) -> int:
    """Prompt until the user enters a valid integer in [lo, hi].

    A parse failure (not a number, or out of range) does not consume one
    of the player's guessing attempts — it just re-prompts.
    """
    while True:
        raw = input(f"Guess a number between {lo} and {hi}: ")
        try:
            return parse_int_in_range(raw, lo, hi)
        except ValueError as exc:
            print(f"Invalid guess: {exc}")


def play_game(
    lo: int = DEFAULT_LOW,
    hi: int = DEFAULT_HIGH,
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    rng: random.Random | None = None,
) -> bool:
    """Run one round of the guessing game. Returns True if the player won.

    `rng` is injectable so this function *could* be tested deterministically
    (pass a seeded `random.Random`) even though, per this week's scope, the
    CLI itself isn't part of the automated test suite.
    """
    rng = rng or random.Random()
    secret = rng.randint(lo, hi)

    print(f"I'm thinking of a number between {lo} and {hi}.")
    print(f"You have {max_attempts} attempts.")

    for attempt in range(1, max_attempts + 1):
        guess = prompt_guess(lo, hi)

        if guess == secret:
            print(f"Correct! The number was {secret}. "
                  f"You got it in {attempt} attempt(s).")
            return True

        remaining = max_attempts - attempt
        if guess < secret:
            print(f"Too low. {remaining} attempt(s) left.")
        else:
            print(f"Too high. {remaining} attempt(s) left.")

    print(f"Out of attempts. The number was {secret}.")
    return False


def main() -> None:
    play_game()


if __name__ == "__main__":
    main()
