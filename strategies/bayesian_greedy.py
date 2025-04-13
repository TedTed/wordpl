# A strategy identical to BayesianRandom (see bayesian_random.py), but instead
# of choosing each guess randomly, it samples from the prior distribution.

from dataclasses import dataclass

from strategies.utils import uniform_prior, update_prior, jitter

@dataclass
class BayesianGreedy:
    epsilon: float
    certainty: float

    def first_move(self):
        self.prior = uniform_prior()
        first_guess = self.prior["word"].sample().item()
        self.past_guesses = [first_guess]
        return first_guess, jitter(self.epsilon)

    def next_move(self, guess, epsilon, clues):
        update_prior(self.prior, guess, epsilon, clues)
        # If we have a winner, return it as a final answer
        best_candidate = self.prior.loc[self.prior["weight"].idxmax()]
        if best_candidate["weight"] > self.certainty:
            return best_candidate["word"], 0
        # If not, sample from the prior distribution, minus words that were
        # already picked as prior guesses.
        possible_guesses = self.prior[~self.prior["word"].isin(self.past_guesses)]
        next_guess = possible_guesses["word"].sample(weights=possible_guesses["weight"])
        self.past_guesses.append(next_guess)
        return next_guess.item(), jitter(self.epsilon)

