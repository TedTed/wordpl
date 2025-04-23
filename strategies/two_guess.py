

# The guess of "trace" solves in 2 guesses 6.48% of the time with perfect clues.
# So, we allocate all the privacy budget to this first guess, then make a best effort on the second guess

# Return a word that is 100% consistent with the clue if possible, otherwise the word with the least
# number of inconsistencies.

from dataclasses import dataclass

MAGIC_WORD = "trace"

@dataclass
class Birdie:
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
