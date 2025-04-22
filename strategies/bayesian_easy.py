# Choose the first clues based on an optimal Wordle solver.
# If the solver doesn't return, sample the next guess from the subjective
# probability distribution, like bayesian_greedy.py.
# Stop when the subjective probability of the answer being true exceeds the
# certainty threshold.

from dataclasses import dataclass

from strategies.wordle_solver_easy import Solver
from strategies.utils import uniform_prior_easy, update_prior, jitter

@dataclass
class BayesianWordleEasy:
    epsilon: float

    def first_move(self):

        self.prior = uniform_prior_easy()
        self.solver = Solver()
        first_guess = self.solver.next_guess().lower()

        # print("First guess:", first_guess)

        self.past_guesses = [first_guess]
        return first_guess, self.epsilon

    def next_move(self, guess, epsilon, clues):
        update_prior(self.prior, guess, epsilon, clues)
        # If we have a winner, return it
        best_candidate = self.prior.loc[self.prior["weight"].idxmax()]

        
        # if best_candidate["weight"] > self.certainty:
        #     return best_candidate["word"], 0

        # if len(self.past_guesses) == 2 and best_candidate["weight"] > 0.3:
        #     return best_candidate["word"], 0

        if len(self.past_guesses) == 2:
            # print("Best candidate:", best_candidate, "weight:", best_candidate["weight"])
            return best_candidate["word"], 0


        # Otherwise, update the Wordle solver
        green = ''.join([guess[i] if clues[i] == 'c' else '_' for i in range(5)])
        yellow = ''.join([guess[i] for i in range(5) if clues[i] == 'i'])
        self.solver.guess(guess, green, yellow)
        # Use the guess suggestion from the solver if there is one
        try:
            next_guess = self.solver.next_guess().lower()
            self.past_guesses.append(next_guess)
            return next_guess, self.epsilon
        # If there is none, fall back to the Bayesian strategy
        except IndexError:
            possible_guesses = self.prior[~self.prior["word"].isin(self.past_guesses)]
            next_guess = possible_guesses["word"].sample(weights=possible_guesses["weight"])
            self.past_guesses.append(next_guess)
            return next_guess.item(), self.epsilon



if __name__ == "__main__":

    # Gather up all the "easy" words -- those that can be guessed reliably in 2 or 3 guesses with optimal strategy

    import re
    pattern = "      [A-Za-z0-9]{6} ([a-z]{5}) GGGGG2"
    pattern2 = "                   [A-Za-z0-9]{6} ([a-z]{5}) GGGGG3"

    words = []
    for line in open("strategy_normal.txt"):
        if re.match(pattern, line):
            words.append(re.match(pattern, line).group(1))
        elif re.match(pattern2, line):
            words.append(re.match(pattern2, line).group(1))

    with open("easy_words.txt", "w") as f:
        for word in set(words):
            f.write(word + "\n")
