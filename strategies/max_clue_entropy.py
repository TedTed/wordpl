# Maximizes the entropy of the conditional clue distribution, given the previous clues.
# Equivalent to minimizing the conditional entropy of the solution given observations.

import itertools as it
import os
from typing import Optional

import numpy as np
from tqdm import tqdm

from strategies.utils import valid, answers, is_consistent


GUESS_LIST = sorted(valid)
SOLUTION_LIST = sorted(answers)
N_CLUES = 3**5


class MaxClueEntropy:
    def __init__(self, n_guesses: int, epsilon_per_guess: float, monte_carlo: Optional[int] = None):
        # Params
        self.total_guesses = n_guesses
        self.epsilon_per_guess = epsilon_per_guess
        self.monte_carlo = monte_carlo
        
        # Constants
        self.clue_matrix = precompute_clue_matrix(cache='cache/clue_matrix.npy')
        self.dist_matrix = precompute_distance_matrix()
        self.all_clue_vecs = np.zeros((N_CLUES, 5), dtype=np.uint8)
        for i in range(N_CLUES):
            self.all_clue_vecs[i] = clue_to_vec(i)

        # Variables
        self.remaining_guesses = n_guesses
        self.prob_s = np.zeros(len(SOLUTION_LIST), dtype=np.float64)
        self.prob_s[:] = 1. / len(SOLUTION_LIST)

    def first_move(self) -> tuple[str, float]:
        self.prob_s[:] = 1. / len(SOLUTION_LIST)
        self.remaining_guesses = self.total_guesses
        return self._regular_move()

    def next_move(self, guess, epsilon, clues):
        self._update_p_s(guess, clues, epsilon)
        self.remaining_guesses -= 1
        if self.remaining_guesses == 0:
            argmax = np.argmax(self.prob_s)
            return SOLUTION_LIST[argmax], 0
        return self._regular_move()
    
    def _regular_move(self) -> tuple[str, float]:
        clue_probs = np.zeros((len(GUESS_LIST), N_CLUES), dtype=np.float64)
        clue_probs[:] = 1e-10
        for i, _ in enumerate(GUESS_LIST):
            if self.monte_carlo:
                js = np.random.choice(len(SOLUTION_LIST), size=self.monte_carlo, p=self.prob_s)
                weights = 1. / (self.monte_carlo * self.prob_s)
            else:
                js = np.arange(len(SOLUTION_LIST))
                weights = np.ones(len(SOLUTION_LIST), dtype=np.float64)
            for j in js:
                clue = self.clue_matrix[i, j]
                n_flipss = self.dist_matrix[clue, :]
                flip_probs = flip_prob(n_flipss, epsilon=self.epsilon_per_guess)
                clue_probs[i] += self.prob_s[j] * flip_probs * weights[j]
        entropies = -np.sum(clue_probs * np.log(clue_probs), axis=1)
        argmax = np.argmax(entropies)
        guess = GUESS_LIST[argmax]
        return guess, self.epsilon_per_guess
    
    def _update_p_s(self, guess: str, clue: str, epsilon: float):
        """Update the solution distribution given the guess and clue."""
        for i, solution in enumerate(SOLUTION_LIST):
            for j, (c, letter) in enumerate(zip(clue, guess)):
                if is_consistent(solution, j, letter, c):
                    self.prob_s[i] *= np.exp(epsilon / 5.)
        self.prob_s /= np.sum(self.prob_s)
    
    def __str__(self):
        return f"MaxClueEntropy(n_guesses={self.total_guesses}, epsilon_per_guess={self.epsilon_per_guess}, monte_carlo={self.monte_carlo})"


def precompute_clue_matrix(cache: Optional[str] = None):
    if cache and os.path.exists(cache):
        print(f"Loading cached clue matrix: {cache}")
        clue_matrix = np.load(cache)
        if clue_matrix.shape != (len(GUESS_LIST), len(SOLUTION_LIST)):
            raise ValueError(f"Cache file {cache} has wrong shape: {clue_matrix.shape}")
        return clue_matrix
    
    print("Precomputing clue matrix...")
    clue_matrix = np.zeros((len(GUESS_LIST), len(SOLUTION_LIST)), dtype=np.uint8)
    iterator = it.product(enumerate(GUESS_LIST), enumerate(SOLUTION_LIST))
    for (i, g), (j, s) in tqdm(iterator, total=clue_matrix.size):
        clue_matrix[i, j] = make_response_code(g, s)
    if cache:
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        print(f"Saving clue matrix to {cache}")
        np.save(cache, clue_matrix)

    return clue_matrix


def precompute_distance_matrix() -> np.ndarray:
    """Precompute the number of flips required between all pairs of clues."""
    print("Precomputing distance matrix...")
    dist_matrix = np.zeros((N_CLUES, N_CLUES), dtype=np.uint8)
    vecs = np.zeros((N_CLUES, 5), dtype=np.uint8)
    for i in range(N_CLUES):
        vecs[i] = clue_to_vec(i)
    for i, j in it.product(range(N_CLUES), repeat=2):
        dist_matrix[i, j] = np.sum(vecs[i] != vecs[j])
    return dist_matrix


def flip_prob(n_flips: int, epsilon: float) -> float:
    """The probability of flipping n clues for a given epsilon."""
    p_flip = 2./ (2. + np.exp(epsilon / 5.))
    p_no_flip = 1. - p_flip
    return p_flip**n_flips * p_no_flip**(5. - n_flips)


def make_response_code(guess: str, solution: str) -> np.uint8:
    """Convert a clue to an unsigned 8-bit integer.
    The clue is the response to a guess for a given solution.
    Each color in the clue is represented by a digit:
    - 0: black
    - 1: yellow
    - 2: green

    The 8-bit integer is then obtained by converting the clue to the five corresponding numbers
    and interpreting them as a base-3 number in Little Endian order.

    For example, the clue "🟩⬛🟨⬛⬛" would be represented as 00102 in base-3, which is
    2 * 3^0 + 0 * 3^1 + 1 * 3^2 + 0 * 3^3 + 0 * 3^4 = 2 + 0 + 9 + 0 + 0 = 11 in decimal.
    """
    preds = np.zeros(5, dtype=np.uint8)
    for idx, (guess_letter, solution_letter) in enumerate(zip(guess, solution)):
        if guess_letter == solution_letter:
            pred = 2
        elif guess_letter in solution:
            pred = 1
        else:
            pred = 0
        preds[idx] = pred
    # convert base-3 representation to int
    return np.sum(preds * 3**np.arange(5), dtype=np.uint8)


def clue_to_vec(clue: np.uint8) -> np.ndarray:
    """Convert a clue number to a 5d vector of 0s, 1s, and 2s."""
    return (clue // 3**np.arange(5)) % 3  # convert int to base-3 representation
