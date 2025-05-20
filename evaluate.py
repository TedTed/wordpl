from datetime import datetime
import math
from pathlib import Path
import random
import signal
import sys

import numpy as np
from tqdm import trange

# Add your new class here
from strategies.g3 import G3
from strategies.d95 import D95

# Instantiate it at most 3 times with different parameters here
STRATEGIES_UNDER_TEST = [
    G3(epsilon1=9.3, epsilon2=5.3), # Current best for 5th percentile
    D95(epsilon=12.3),
    D95(epsilon=25.0),
]

NUM_TRIALS = 10001
TIMEOUT_DURATION = 10

with open("valid.txt", "r") as f:
    valid = set(f.read().splitlines())

with open("answers.txt", "r") as f:
    answers = f.read().splitlines()

timeout = Exception("timeout!")

def raise_timeout(signum, frame):
    raise timeout

def evaluate(strategy, num_trials, debug=False):
    """Evaluates a strategy over multiple trials.

    `strategy` must be an object of a class implementing two methods:
    - `first_move` takes no arguments and returns a `(guess, epsilon)` pair,
    representing the player's first move.
    - `next_move` takes three arguments `guess`, `epsilon`, and `result`. The
    first two are the player's previous move; the third is the game's response
    for this move. This response is guaranteed to be a five-letter string where
    each char is either:
    - 'c': the corresponding letter is in the same position in the secret answer
    - 'i': the corresponding letter is in the secret answer, but not at this
      position
    - '.': the corresponding letter is not in the secret answer
    Of course, this being a DP game, the result is randomized: each letter has a
    probability 2/(2+exp(epsilon/5)) to be randomly switched to one of the two
    other possible letters.

    Guesses must always be five-letter strings who are in the `valid.txt` word
    list. Epsilon values must be nonnegative; an epsilon value of 0 represents the
    player's final guess.

    Returns a tuple with five elements: the list of scores, the 5th, 50th,
    and 95th percentiles of the scores, and the number of timeouts.
    """
    scores = []
    timeouts = 0
    for _ in trange(num_trials, smoothing=0):
        try:
            signal.signal(signal.SIGALRM, raise_timeout)
            signal.alarm(TIMEOUT_DURATION)
            scores.append(evaluate_once(strategy, debug))
        except Exception as e:
            if e == timeout:
                timeouts += 1
            else:
                print(f"Encountered exception {e}")
                import traceback
                traceback.print_exc()
            scores.append(float('inf'))
    if timeouts > 0:
        print(f"Evaluation timed out {timeouts} times")
    return (
        scores,
        quantile(scores, 0.05),
        quantile(scores, 0.5),
        quantile(scores, 0.95),
        timeouts,
    )

def quantile(a, q):
    # numpy's quantile gets confused when there are infinity values. So we
    # convert all of them to a very large float, and then convert back very
    # large values to infinity.
    r = np.quantile([sys.float_info.max if math.isinf(x) else x for x in a], q)
    if r > sys.float_info.max/100:
        return float('inf')
    return r

def evaluate_once(strategy, debug=False, end_message=False):
    """Evaluates a strategy once.

    Returns float('inf') if the final guess of the strategy is wrong; otherwise,
    returns the total epsilon budget consumed by the strategy.

    If debug is True, prints all the player moves, and the real vs. noisy clues
    at each turn.

    If end_message is true, prints the answer at the end of the game indicating
    whether the player won or lost.
    """
    answer = random.choice(answers)

    if debug:
        print(f"Real answer: '{answer}'")
    guess, epsilon = strategy.first_move()
    total_epsilon = 0

    # Answer as many guesses as requested
    while epsilon > 0:
        if guess not in valid:
            raise ValueError(f"guess '{guess}' is not in the valid.txt word list")
        total_epsilon += epsilon
        real_clues = ''
        for (i, letter) in enumerate(guess):
            if letter == answer[i]:
                real_clues += 'c'
            elif letter in answer:
                real_clues += 'i'
            else:
                real_clues += '.'
        noisy_clues = ''
        for a in real_clues:
            # Choose randomly with probability 3/(2+e^(ε/5)); equivalent to choosing
            # randomly *among the incorrect options* with probability 2/(2+e^(ε/5)).
            if random.random() < 3./(2.+math.exp(epsilon/5)):
                noisy_clues += random.choice(['c', 'i', '.'])
            else:
                noisy_clues += a
        if debug:
            print(f"Guess '{guess}' with epsilon={epsilon}")
            print(f"  Real clues: '{real_clues}'")
            print(f"  Noisy clues: '{noisy_clues}'")
        guess, epsilon = strategy.next_move(guess, epsilon, noisy_clues)

    # Check final answer
    if guess == answer:
        if debug or end_message:
            print(f"Final guess '{guess}' is correct! :D")
            print(f"Used a total epsilon of '{total_epsilon}'.")
        return total_epsilon

    if debug or end_message:
        print(f"Final guess '{guess}' is incorrect =(")
        print(f"True answer was '{answer}'.")
    return float('inf')

if __name__ == "__main__":
    time = datetime.now().strftime("%Y-%m-%d-%Hh%Mm%Ss")
    Path("results").mkdir(exist_ok=True)
    output_path = f"results/results-{time}.csv"
    with open(output_path, "a") as output:
        output.write("strategy;p05;p50;p95;timeouts\n")
    for strat in STRATEGIES_UNDER_TEST:
        print(f"Testing strategy {strat}…")
        (scores, p05, p50, p95, timeouts) = evaluate(strat, NUM_TRIALS)
        print(f"5th percentile: {p05}")
        print(f"50th percentile: {p50}")
        print(f"95th percentile: {p95}")
        print(f"timeouts: {timeouts}")
        with open(output_path, "a") as output:
            output.write(f"{strat};{p05};{p50};{p95};{timeouts}\n")








