# WORDPL — Strategy contest version

This is a Python implementation of
[WORDPL](https://www.oblivious.com/games/wordpl), a variant of
[Wordle](https://www.nytimes.com/games/wordle/index.html) developed by the team
at [Oblivious](https://www.oblivious.com/). The goal is to find out a strategy
that achieves a score as low as possible with some probability.

The game and the strategy contest (with prizes!) is discussed in more detail in
[this blog post](https://desfontain.es/blog/wordpl.html).

## Current leaderboard

TODO

## Game rules

The game selects a *secret word* at random among the words in `answers.txt`. The
goal of the player is to find this secret word.

Each round, the player can take one of two actions.

- Get clues: the player selects a five-letter word in `valid.txt` (the *guess*),
  and an `epsilon` value. The game then generates five clues — one per letter.

  - 'c' means that the secret word contains this letter, at this position.
  - 'i' means that the secret word contains this letter, but not at this
    position.
  - '.' means that the secret word does not contain this letter.

  Then, the game *randomizes* these clues. Each clue stays unchanged with
  probability `exp(epsilon/5)/(2+exp(epsilon/5))`, and is changed to one of
  other two clues with probability `1/(2+exp(epsilon/5))`.

  The randomized clues are then returned to the player as a 5-character string.

- Propose an answer: the player selects a five-letter word in `answers.txt` (the
  *final guess*). This stops the game.

  - If the final guess is the secret word, the player wins. Their score is the
    sum of all the `epsilon` values used in previous rounds.
  - If the final guess is not the secret word, the player loses. Their score is
    +∞.

## Implementing a strategy

A strategy is an instance of a class that implements two methods:

- `first_move` takes no arguments and returns a `(guess, epsilon)` pair,
  representing the player's first move.
- `next_move` takes three arguments `guess`, `epsilon`, and `result`, and
  returns a `(next_guess, next_epsilon)` pair. The first two are the player's
  previous move; the third is the game's response for this previous move. The
  method returns the player's next move.

To get clues, the player must return a strictly positive `epsilon`. To propose
an answer, the player must return an `epsilon` value of `0`.

It is recommended to have your strategy class also implement `__str__`, so it
appears in a human-readable way in scoring reports.

You can see a simple strategy example in
[`strategy/bayesian_random.py`](./strategy/bayesian_random.py).

## Scoring a strategy

To score your strategy, import it from `evaluate.py`, and add one or more
instances of it to `STRATEGIES_UNDER_TEST`. Then, run `python evaluate.py`. The
results are written to a CSV file stored in a `results` directory. Note that to
make sure evaluation doesn't take too long, each game must terminate within 5
seconds. Past this delay, we consider that the player has lost.

Running this code requires Python (I tried it with Python 3.10, but any
reasonably recent version should work) and a fairly minimal set of dependencies,
which you can install using `pip`:

```
pip install numpy pandas tqdm
```

## Acknowledgments

Thanks to Josh Wardle for inventing Wordle, to the folks at
[Oblivious](https://www.oblivious.com/) for coming up with this fun variant, and
to [Josh Stephenson](https://github.com/joshstephenson) for creating the Python
[Wordle solver](https://github.com/joshstephenson/Wordle-Solver) that I rely on
for my initial attempt at a good strategy.
