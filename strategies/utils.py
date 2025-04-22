from math import exp
from random import uniform
import pandas as pd

with open("valid.txt", "r") as f:
    valid = f.read().splitlines()

with open("answers.txt", "r") as f:
    answers = f.read().splitlines()

with open("easy_words.txt", "r") as f:
    easy_words = f.read().splitlines()

def uniform_prior():
    prior = pd.DataFrame({"word": answers})
    prior["weight"] = 1
    return prior

def uniform_prior_easy():
    prior = pd.DataFrame({"word": easy_words})
    prior["weight"] = 1
    return prior

def update_prior(prior, guess, epsilon, clues):
    for index, clue in enumerate(clues):
        prior["weight"] = prior.apply(
            lambda row: update_weight(row, index, guess[index], clue, epsilon),
            axis=1)
    # normalizing the distribution is not
    prior["weight"] = prior["weight"] / sum(prior["weight"])
    return prior

# Check whether a given clue is consistent with a word.
def is_consistent(word, index, letter, clue):
    if clue == ' ':
        return letter not in word
    if clue == 'i':
        return letter in word and word[index] != letter
    if clue == 'c':
        return word[index] == letter

# Updates the weight associated with a word based on a clue
def update_weight(row, index, letter, clue, epsilon):
    if is_consistent(row["word"], index, letter, clue):
        return row["weight"]*exp(epsilon/5)
    return row["weight"]

# Returns the input randomized up to ±10%
def jitter(x):
    return uniform(x*0.9, x*1.1)
