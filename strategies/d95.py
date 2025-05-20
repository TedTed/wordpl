
from dataclasses import dataclass
import json
import numpy as np
import os
from math import exp
from numba import njit, prange

second_move_strategy_12 = [5699, 839, 4669, 7411, 3634, 11242, 10666, 3974, 3738, 9085, 11838, 5878, 5764, 7411, 6963, 7911, 7911, 11779, 12356, 12132, 258, 3716, 2136, 4827, 3308, 9249, 1365, 10937, 3634, 6060, 5575, 3634, 12680, 8543, 7650, 8410, 7411, 10937, 12423, 6750, 7911, 6963, 7911, 7911, 11779, 11737, 3477, 2736, 6422, 12282, 12393, 7650, 7650, 9936, 6449, 9333, 5860, 2076, 6363, 12367, 3346, 4874, 6961, 5422, 9085, 9198, 5764, 11758, 12367, 8220, 8220, 1055, 5918, 7675, 8467, 12617, 3428, 650, 10340, 83, 2925, 11006, 839, 3664, 9003, 2244, 7870, 3492, 1392, 1652, 5459, 9959, 11911, 5459, 12686, 7870, 3492, 10661, 653, 5835, 9752, 6495, 4827, 2684, 4827, 3944, 10661, 7955, 5459, 3634, 5101, 5459, 3634, 6979, 6528, 10982, 12485, 5459, 11443, 29, 5459, 3634, 12158, 12949, 10982, 1114, 12288, 5835, 3517, 12288, 7605, 6979, 4660, 4660, 2491, 4653, 952, 7729, 718, 1174, 3474, 8433, 622, 6961, 12796, 8054, 692, 5422, 6775, 1707, 12214, 8737, 8857, 4653, 11691, 11781, 718, 1174, 12365, 4726, 622, 319, 839, 839, 3664, 8878, 9015, 8878, 3913, 10677, 8710, 2719, 9959, 3858, 4033, 9015, 11118, 9901, 4229, 18, 11582, 11582, 2839, 2163, 4929, 5517, 4910, 2096, 6372, 1454, 1454, 12262, 3500, 10221, 11765, 10423, 4513, 12960, 988, 6042, 12964, 988, 5285, 4979, 12803, 10868, 12958, 2163, 12519, 6252, 9113, 2163, 6245, 2567, 2567, 5568, 952, 952, 5500, 12625, 6775, 11306, 3911, 11468, 3805, 3913, 3913, 7487, 6920, 6775, 2827, 2131, 3913, 8342, 10990, 9411, 5270, 11334, 6525, 6137, 5356, 9791, 11082]
second_move_strategy_27 = [9897, 3216, 6659, 11242, 3634, 11242, 4887, 5477, 2188, 9085, 9959, 5878, 5764, 9015, 6963, 7911, 8220, 5219, 1079, 6165, 5385, 12617, 12155, 5517, 6441, 2757, 2459, 10937, 3041, 12804, 8543, 7478, 12680, 12398, 6451, 7539, 988, 10937, 12423, 11268, 7911, 3816, 7911, 7911, 12366, 12356, 3041, 9879, 6422, 12282, 6145, 7650, 12117, 9936, 3707, 890, 5634, 2076, 5074, 6000, 6898, 9302, 6161, 5422, 9085, 9198, 5764, 834, 6728, 8220, 4874, 12254, 8386, 9333, 8467, 12617, 4397, 2411, 6960, 782, 747, 12131, 9752, 3664, 9003, 10253, 11214, 12214, 7497, 1652, 5459, 3509, 11911, 7870, 10253, 7870, 1375, 10661, 653, 269, 9752, 12672, 9354, 2684, 331, 3944, 10661, 2277, 5459, 3634, 7672, 7909, 3634, 6979, 8410, 10982, 6269, 5459, 11443, 29, 5459, 3634, 12158, 9880, 12214, 1114, 12838, 2199, 5350, 4630, 5106, 2099, 8576, 4660, 11937, 4653, 6171, 6946, 4463, 12082, 7343, 4726, 5011, 10605, 9587, 347, 7737, 3880, 9661, 2730, 8433, 10953, 6601, 2545, 11691, 2591, 10815, 5432, 7435, 4726, 9136, 8395, 2969, 839, 10140, 5451, 8187, 3040, 3120, 1404, 2205, 2719, 9959, 12829, 577, 9015, 11118, 5451, 4331, 18, 1269, 5485, 7858, 11334, 4929, 10948, 6903, 12634, 6372, 8213, 1454, 12883, 3500, 10221, 2143, 12803, 4513, 8710, 988, 6042, 12564, 11217, 12642, 10415, 2922, 10868, 8055, 2163, 12519, 7365, 2717, 5392, 6245, 11053, 2567, 5568, 10475, 9411, 9303, 3279, 243, 11306, 5401, 5722, 3805, 9756, 4874, 10571, 413, 6775, 2827, 2669, 11468, 8342, 3729, 10224, 4943, 1269, 6525, 7211, 5356, 9889, 11082]

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


@njit(parallel=True)
def best_third_guess(w1, c1, w2, c2):

    # likelihood of answer a given w1, c1, w2, c2
    lia = np.zeros(NAW)
    for a in range(NAW):
        lia[a] = pd[c1][cwa[w1][a]] * pd[c2][cwa[w2][a]]
    slia = np.argsort(lia)
    possible_answers = slia[-int(NAW / 50):]

    expected_wins = np.zeros(NVW)

    for w3 in prange(NVW):
        total_expected_wins = 0
        for c3 in range(3**5):
            bew = 0
            for a in possible_answers:
                bew = max(bew, pd[c1][cwa[w1][a]] * pd[c2][cwa[w2][a]] * pd[c3][cwa[w3][a]])
            total_expected_wins += bew
        expected_wins[w3] = total_expected_wins

    return np.argmax(expected_wins)


@njit(parallel=True)
def best_final_guess(w1, c1, w2, c2, w3, c3):
    """
    Compute the final guess with the highest expected wins after playing the words w1, w2, w3 and
    getting clues c1, c2, c3.
    """
    expected_wins = np.zeros(NAW)
    for a in prange(NAW):
        expected_wins[a] = pd[c1][cwa[w1][a]] * pd[c2][cwa[w2][a]] * pd[c3][cwa[w3][a]]
    return np.argmax(expected_wins)


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

        if self.epsilon < 20:
            self.second_move_strategy = second_move_strategy_12
        else:
            self.second_move_strategy = second_move_strategy_27

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
            guess = self.second_move_strategy[self.clues[0]]
            self.guesses.append(guess)
            return valid_words[guess], self.epsilon
        elif turn == 3:
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
