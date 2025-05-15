
from dataclasses import dataclass
import json
import os
from math import exp
import numpy as np

ws1 = "trace"
strategy = [4205, 4300, 8266, 12031, 7702, 11987, 11983, 11173, 7033, 7286, 7395, 2680, 3546, 12737, 12603, 9400, 2115, 6539, 9888, 3009, 7731, 10458, 1372, 960, 2402, 1307, 9180, 8523, 974, 1748, 5368, 11133, 1748, 3038, 12643, 9561, 1015, 5312, 999, 1015, 269, 1677, 11642, 5312, 6131, 10871, 7207, 10871, 3523, 917, 9589, 887, 11598, 12874, 12693, 6776, 3756, 3908, 5057, 49, 10797, 5864, 9667, 5827, 75, 4331, 4242, 7702, 12603, 11097, 3934, 2816, 3670, 4654, 10125, 49, 6244, 1676, 6759, 11296, 9191, 2484, 8872, 12842, 9475, 5625, 8512, 4698, 9096, 2108, 6614, 156, 11262, 2513, 9502, 6855, 9400, 11878, 12021, 7398, 10149, 8517, 89, 10688, 994, 7696, 11072, 12899, 11879, 10645, 7883, 304, 9354, 10092, 2356, 1700, 7883, 4929, 3336, 5313, 11582, 11582, 156, 8195, 1454, 1943, 622, 6857, 2025, 3523, 8963, 9800, 622, 4696, 4232, 1167, 11346, 12949, 12400, 4822, 3325, 73, 7310, 10398, 2219, 7702, 10861, 4959, 5972, 3546, 1113, 988, 9164, 5007, 413, 7067, 5007, 11597, 12218, 8802, 2076, 9432, 10283, 4627, 705, 8540, 1991, 1455, 3886, 4074, 9809, 5832, 4542, 4690, 4087, 12360, 4690, 3044, 4164, 11596, 5344, 7388, 10458, 5733, 7047, 3045, 11724, 1307, 950, 2465, 10140, 12026, 11937, 6099, 4328, 4017, 3957, 6033, 5508, 5540, 7454, 5089, 269, 11816, 1802, 9954, 12010, 3314, 7429, 3496, 6313, 6645, 6556, 9432, 12246, 6961, 2955, 9784, 1071, 2884, 5301, 5467, 6017, 3258, 5739, 3678, 11387, 10821, 4771, 2439, 4057, 8075, 2519, 3738, 1085, 7837, 319, 2250, 2866, 8802, 322, 8483, 6961]

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

def pd(epsilon):
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


def best_final_guess(w1, c1, w2, c2):

    ps1 = pd1[c1][cwa[w1]]
    ps2 = pd2[c2][cwa[w2]]
    ps3 = ps1 * ps2
    ps3 = ps3[:, np.newaxis]

    return np.argmax(ps3)


pd1 = None
pd2 = None
cwa = None

@dataclass
class G3:
    epsilon1: float
    epsilon2: float

    def __post_init__(self):
        global pd1
        global pd2
        global cwa
        pd1 = pd(self.epsilon1)
        pd2 = pd(self.epsilon2)
        cwa = compute_cwa(cache_filepath="strategies/cwa.txt")


    def first_move(self):
        self.guesses = [valid_words.index(ws1)]
        self.clues = []
        return ws1, self.epsilon1

    def next_move(self, guess, epsilon, clues):
        self.clues.append(clue_str_to_int(clues))
        turn = len(self.guesses) + 1

        if turn == 2:
            guess = strategy[self.clues[0]]
            self.guesses.append(guess)
            return valid_words[guess], self.epsilon2
        else:
            guess = best_final_guess(self.guesses[0], self.clues[0], self.guesses[1], self.clues[1])
            return answers[guess], 0


