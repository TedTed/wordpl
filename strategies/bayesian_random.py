# A very simple strategy for WORDPL. Takes two parameters as input:
#
# - epsilon: the average epsilon used for each of the player's guesses
# - certainty: when the probability of one possible answer being correct becomes
#   larger than this threshold, use this answer as a final guess
#
# The strategy then works as follows.
#
# 1. Initialize a uniform Bayesian prior over all possible answers
# 2. Pick a random word as a guess, using the fixed epsilon
# 3. Update the Bayesian prior according to the answer
# 4. If more than `certainty` of the total probability mass is concentrated on a
#    single answer, return this answer. Otherwise, go back to 2.

from dataclasses import dataclass
import random

from strategies.utils import valid, answers, uniform_prior, update_prior, jitter

@dataclass
class BayesianRandom:
    epsilon: float
    certainty: float

    def first_move(self):
        self.prior = uniform_prior()
        return random.choice(valid), self.epsilon

    def next_move(self, guess, epsilon, clues):
        update_prior(self.prior, guess, epsilon, clues)
        # If we have a winner, return it as a final answer
        best_candidate = self.prior.loc[self.prior["weight"].idxmax()]
        if best_candidate["weight"] > self.certainty:
            return best_candidate["word"], 0
        # If not, pick a new random word
        return random.choice(valid), self.epsilon

