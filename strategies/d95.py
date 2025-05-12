
from dataclasses import dataclass
import json
import numpy as np
import os
from math import exp


with open("strategies/d95.json", "r") as f:
    second_move_strategy = json.load(f)

with open("strategies/d953.json", "r") as f:
    third_move_strategy_str = json.load(f)

third_move_strategy = {}

# since json doesn't support integer keys
for c1, s in third_move_strategy_str.items():
    for c2, w3 in s.items():
        if int(c1) not in third_move_strategy:
            third_move_strategy[int(c1)] = {}
        third_move_strategy[int(c1)][int(c2)] = w3

valid_words = open("valid.txt", "r").read().splitlines()
answers = open("answers.txt", "r").read().splitlines()

NAW = len(answers)
NVW = len(valid_words)
VW = range(NVW)
AW = range(NAW)

def clue(guess, answer):
    real_clues = ""
    for (i, letter) in enumerate(guess):
        if letter == answer[i]:
            real_clues += '0' # c
        elif letter in answer:
            real_clues += '1' # i
        else:
            real_clues += '2' # .
    return int(real_clues, 3)

def clue_str_to_int(s):
    t = str.maketrans("ci.GYB", "012012")
    return int(s.translate(t), 3)

def clue_diffs(c1, c2):
    diffs = 0
    for i in range(5):
        if c1 % 3 != c2 % 3:
            diffs += 1
        c1 //= 3
        c2 //= 3
    return diffs

def clue_to_str(n):
    if n == 0:
        return "ccccc"
    digits = []
    while n:
        digits.append(str(n % 3))
        n //= 3
    s = ''.join(digits[::-1])
    t = str.maketrans("012", "ci.")
    # left pad with cs to make it 5 digits
    return s.zfill(5).translate(t)

def compute_cwa(cache_filepath="data/cwa.txt"):
    """
    The clue for each valid word and answer, stored in a compact base 3 integer

    cwa[guess_word][answer_word]: clue 

    """

    cwa = []
    if not os.path.exists(cache_filepath):
        for gw in valid_words:
            row = []
            for aw in answers:
                row.append(clue(gw, aw))
            cwa.append(row)
        with open(cache_filepath, "w") as f:
            for row in cwa:
                f.write(" ".join(map(str, row)) + "\n")
    else:
        with open(cache_filepath, "r") as f:
            cwa = [list(map(int, line.split())) for line in f]

    cwa = np.array(cwa)
    return cwa

def d():
    """
    d[clue1][clue2]: count of letters that are different between clue1 and clue2
    """

    dm = []
    for c1 in range(3**5):
        row_d = []
        for c2 in range(3**5):
            dd = sum(1 for a, b in zip(clue_to_str(c1), clue_to_str(c2)) if a != b)
            row_d.append(dd)
        dm.append(row_d)

    return np.array(dm)

def compute_pd(epsilon):
    """
    pd[clue1][clue2]: the probability of getting a clue given an actual clue
    """
    dm = d()
    pd = []
    # probability of a correct clue
    pc = 1 - 2.0 / (2.0 + exp(epsilon / 5.0))

    # probability of a particular incorrect clue
    pi = 1.0 / (2.0 + exp(epsilon / 5.0))
    n = 5

    for c1 in range(3**5):
        row_pd = []
        for c2 in range(3**5):
            dd = dm[c1][c2]
            k = 5 - dd
            p = pc**k * (pi**(n-k))
            row_pd.append(p)
        pd.append(row_pd)

    return np.array(pd)


def best_third_guess(w1, c1, w2, c2):
    """
    Compute the expected wins for every possible third guess after playing words w1, w2 and getting clues c1, c2.

    Return the one with the highest expected wins.
    """

    ps1 = pd[c1][cwa[w1]]
    ps2 = pd[c2][cwa[w2]]
    ps = ps1 * ps2
    ps = ps[:, np.newaxis]

    best_w3 = None
    best_expected_wins = 0

    for w3 in range(NVW):

        ps3 = pd[:][cwa[w3]]
        ps4 = ps * ps3
        expected_wins = np.sum(np.max(ps4, axis=0))

        if expected_wins >= best_expected_wins:
            best_expected_wins = expected_wins
            best_w3 = w3

    return best_w3

def best_final_guess(w1, c1, w2, c2, w3, c3):
    """
    Compute the final guess with the highest expected wins after playing the words w1, w2, w3 and
    getting clues c1, c2, c3.
    """
    ps1 = pd[c1][cwa[w1]]
    ps2 = pd[c2][cwa[w2]]
    ps3 = pd[c3][cwa[w3]]
    ps4 = ps1 * ps2 * ps3
    ps4 = ps4[:, np.newaxis]

    return np.argmax(ps4)


pd = None
cwa = None

@dataclass
class D95:
    epsilon: float

    def __post_init__(self):
        global pd
        global cwa

        pd = compute_pd(self.epsilon)
        cwa = compute_cwa(cache_filepath="strategies/cwa.txt")

    def first_move(self):
        ws1 = "salet"
        w1 = valid_words.index(ws1)

        self.guesses = [w1]
        self.clues = []
        return "salet", self.epsilon

    def next_move(self, guess, epsilon, clues):
        self.clues.append(clue_str_to_int(clues))
        turn = len(self.guesses) + 1

        if turn == 2:
            guess = second_move_strategy[self.clues[0]]
            self.guesses.append(guess)
            return valid_words[guess], self.epsilon
        elif turn == 3:
            try:
                guess = third_move_strategy[self.clues[0]][self.clues[1]]    
            except KeyError:
                guess = best_third_guess(self.guesses[0], self.clues[0], self.guesses[1], self.clues[1])
            
            self.guesses.append(guess)
            return valid_words[guess], self.epsilon
        else:
            guess = best_final_guess(
                self.guesses[0], self.clues[0],
                self.guesses[1], self.clues[1],
                self.guesses[2], self.clues[2]
            )
            return answers[guess], 0
