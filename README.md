# WORDPL — Strategy contest version

This is a Python implementation of
[WORDPL](https://games.oblivious.com/games/wordpl), a variant of
[Wordle](https://www.nytimes.com/games/wordle/index.html) developed by the team
at [Oblivious](https://www.oblivious.com/). The goal of each game is to find the
secret word with the smallest possible privacy budget. The goal of the contest
is to create a strategy that does this with sufficiently high probability.

The game and the strategy contest (with prizes!) is discussed in more detail in
[this blog post](https://desfontain.es/blog/wordpl.html).

## Current best scores

| Type of score   | Strategy                                           | Total budget |
| --------------- | -------------------------------------------------- | ------------ |
| 5th percentile  | [`TwoGuess(epsilon=17.9)`][tg]                     | 17.9         |
| 50th percentile | [`BayesianWordle(epsilon=16, certainty=0.3)`][bw]  | 66.6         |
| 95th percentile | [`BayesianWordle(epsilon=30, certainty=0.7)`][bw]  | 153.9        |

[tg]: ./strategies/two_guess.py
[tg]: ./strategies/bayesian_wordle.py

If you can find a strategy that improves one or more of these high scores by at
least 5%, you win a Swiss chocolate bar 🍫 from my favorite chocolate shop in
Zürich.

## Game rules

The game selects a *secret word* at random among the words in `answers.txt`. The
goal of the player is to find this secret word.

Each round, the player can take one of two actions.

- Get clues: the player selects a five-letter word in `valid.txt` (the *guess*),
  and an `epsilon` value. The game then generates five clues — one per letter.

  - `'c'` means that the secret word contains this letter, at this position.
  - `'i'` means that the secret word contains this letter, but not at this
    position.
  - `'.'` means that the secret word does not contain this letter.

  Then, the game *randomizes* these clues. Each clue stays unchanged with
  probability `exp(epsilon/5)/(2+exp(epsilon/5))`, and is changed to one of
  other two clues with probability `1/(2+exp(epsilon/5))`.

  The randomized clues are then returned to the player as a 5-character string.

- Propose an answer: the player selects a five-letter word in `answers.txt` (the
  *final guess*). This stops the game.

  - If the final guess is the secret word, the player wins. Their score is the
    sum of all the `epsilon` values used in previous rounds.
  - If the final guess is not the secret word, the player loses. Their score is
    +∞ (`float('inf')`).

You can run `python interactive.py` to play this version of the game.

## Implementing a strategy

First, install some dependencies:

```
pip install numpy pandas tqdm
```

Then, create a new file in the `strategies` directory, and create a Python class
that implements two methods:

- `first_move(self)` must return a `(guess, epsilon)` pair, representing the
  player's first move. `guess` must be a five-character word in `valid.txt`, and
  `epsilon` must be a nonnegative number.
- `next_move(guess, epsilon, result)` must return a `(next_guess, next_epsilon)`
  pair, representing the player's next move. The `guess` and `epsilon` arguments
  are the player's previous move; the third is the game's response for this
  previous move.

To get clues, the player must return a strictly positive `epsilon`. To propose
an answer, the player must return an `epsilon` value of `0`.

It is recommended to have your strategy class also implement `__str__`, so it
appears in a human-readable way in scoring reports.

You can see a simple strategy example in
[`strategies/bayesian_random.py`](./strategies/bayesian_random.py).

## Scoring a strategy

To score your strategy, import it from `evaluate.py`, and add some instances of
it to `STRATEGIES_UNDER_TEST`. Then, run `python evaluate.py`. The results are
written to a CSV file stored in a `results` directory.

If your strategy beats a high score, send a PR to add it to this repo. I'll run
it on my machine to confirm the score and add you to the leaderboard. Bonus
points if you also write a blog post to explain your approach — I'm happy to
host it if that's convenient for you.

Note that to make sure evaluation doesn't take too long, each game must
terminate within 5 seconds. Past this delay, we consider that the player has
lost. If this ends up being a significant factor in some strategies being better
than others, I'll reconsider it.

## Acknowledgments

Thanks to Josh Wardle for inventing Wordle, to the folks at
[Oblivious](https://www.oblivious.com/) for coming up with this fun variant, and
to [Josh Stephenson](https://github.com/joshstephenson) for creating the Python
[Wordle solver](https://github.com/joshstephenson/Wordle-Solver) that I rely on
for my initial attempt at a good strategy.
