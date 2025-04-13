# Choose the first clues based on an optimal Wordle solver.
# If the solver doesn't return, choose randomly.

from dataclasses import dataclass

from strategies.wordle_solver import Solver
from strategies.utils import uniform_prior, update_prior, jitter

@dataclass
class BayesianWordle:
    epsilon: float
    certainty: float

    def first_move(self):
        self.prior = uniform_prior()
        self.solver = Solver()
        first_guess = self.solver.next_guess().lower()
        self.past_guesses = [first_guess]
        return first_guess, jitter(self.epsilon)

    def next_move(self, guess, epsilon, clues):
        update_prior(self.prior, guess, epsilon, clues)
        # If we have a winner, return it
        best_candidate = self.prior.loc[self.prior["weight"].idxmax()]
        if best_candidate["weight"] > self.certainty:
            return best_candidate["word"], 0
        # Otherwise, update the Wordle solver
        green = ''.join([guess[i] if clues[i] == 'c' else '_' for i in range(5)])
        yellow = ''.join([guess[i] for i in range(5) if clues[i] == 'i'])
        self.solver.guess(guess, green, yellow)
        # Use the guess suggestion from the solver if there is one
        try:
            next_guess = self.solver.next_guess().lower()
            self.past_guesses.append(next_guess)
            return next_guess, jitter(self.epsilon)
        # If there is none, fall back to the Bayesian strategy
        except IndexError:
            possible_guesses = self.prior[~self.prior["word"].isin(self.past_guesses)]
            next_guess = possible_guesses["word"].sample(weights=possible_guesses["weight"])
            self.past_guesses.append(next_guess)
            return next_guess.item(), jitter(self.epsilon)

