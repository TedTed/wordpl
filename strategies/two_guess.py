

# The guess of "trace" solves in 2 guesses 6.48% of the time with perfect clues.
# So, we allocate all the privacy budget to this first guess, then make a best effort on the second guess

# Return a word that is 100% consistent with the clue if possible, otherwise the word with the least
# number of inconsistencies.

from dataclasses import dataclass
import math
import random
from tqdm import tqdm
MAGIC_WORD = "trace"

@dataclass
class TwoGuess:
    epsilon: float

    def first_move(self):
        return MAGIC_WORD, self.epsilon

    def next_move(self, guess, epsilon, clues):

        if clues.startswith("ccccc"):
            return MAGIC_WORD, 0

        # pick word that is consistent with the clue
        words = open("answers.txt").read().splitlines()

        word_scores = []

        for word in words:
            word_score = 5

            for i in range(5):
                cg = MAGIC_WORD[i]
                cw = word[i]
                c = clues[i]

                if c == "c":
                    if cg != cw:
                        word_score -= 1
                elif c == "i":
                    if cg == cw:
                        word_score -= 1
                    elif cg not in word:
                        word_score -= 1
                elif c == ".":
                    if cg in word:
                        word_score -= 1

            word_scores.append((word, word_score))

        word_scores.sort(key=lambda x: x[1], reverse=True)

        return word_scores[0][0], 0


if __name__ == "__main__":
    
    trials = 1000
    epsilon = 17.85
    score = 0

    starting_word = "trace"

    # Best starting words (found by exhaustive search):
    # trace 6.48
    # crate 6.39
    # salet 6.39
    # reast 6.35
    # slate 6.35
    # carte 6.31
    # parse 6.31
    # caret 6.26
    # peart 6.26
    # carle 6.22

    answers = open("answers.txt").read().splitlines()

    clue_memo = {}

    def get_clue(guess, answer, epsilon = None):
        real_clues = ''
        if (guess, answer) in clue_memo:
            real_clues = clue_memo[(guess, answer)]

        else:
            for (i, letter) in enumerate(guess):
                if letter == answer[i]:
                    real_clues += 'c'
                elif letter in answer:
                    real_clues += 'i'
                else:
                    real_clues += '.'
            clue_memo[(guess, answer)] = real_clues

        if epsilon is None:
            return real_clues

        noisy_clues = ''
        for a in real_clues:
            # Choose randomly with probability 3/(2+e^(ε/5)); equivalent to choosing
            # randomly *among the incorrect options* with probability 2/(2+e^(ε/5)).
            if random.random() < 3./(2.+math.exp(epsilon/5)):
                noisy_clues += random.choice(['c', 'i', '.'])
            else:
                noisy_clues += a

        return noisy_clues


    guess_memo = {}

    def compute_guess(guess, clue):

        if (guess, clue) in guess_memo:
            return guess_memo[(guess, clue)]

        word_scores = []
        for word in answers:
            word_score = 5
            for i in range(5):
                cg = guess[i]
                cw = word[i]
                c = clue[i]
                if c == "c":
                    if cg != cw:
                        word_score -= 1
                elif c == "i":
                    if cg == cw:
                        word_score -= 1
                    elif cg not in word:
                        word_score -= 1
                elif c == ".":
                    if cg in word:
                        word_score -= 1

            word_scores.append((word, word_score))
        word_scores.sort(key=lambda x: x[1], reverse=True)
        guess_memo[(guess, clue)] = word_scores[0][0]
        return word_scores[0][0]

    for answer in tqdm(answers):
        for _ in range(trials):
            clue = get_clue(starting_word, answer, epsilon=epsilon)
            guess = compute_guess(starting_word, clue)

            if guess == answer:
                score += 1

    print(f"At epsilon={epsilon}, {score / (len(answers) * trials) * 100:.4f}% of games are won")
