from evaluate import evaluate_once

with open("valid.txt", "r") as f:
  valid = set(f.read().splitlines())

def ask(message):
    try:
        return input(message)
    except KeyboardInterrupt:
        exit(0)

def ask_guess():
    guess = ask(f"New guess? ")
    if guess == '':
        return suggested_guess
    if guess not in valid:
        print("guess '{guess}' is not in the valid.txt word list, try again")
        return ask_guess()
    return guess

def ask_epsilon():
    eps = ask(f"New epsilon? ")
    try:
        return float(eps)
    except ValueError:
        print("Could not parse epsilon, try again")
        return ask_epsilon()

class Interactive:
    def first_move(self):
        guess = ask_guess()
        epsilon = ask_epsilon()
        return guess, epsilon

    def next_move(self, guess, epsilon, answer):
        print(f"Answer: '{answer}'")
        print()
        guess = ask_guess()
        epsilon = ask_epsilon()
        return guess, epsilon

if __name__ == "__main__":
    strategy = Interactive()
    score = evaluate_once(strategy, end_message=True)
