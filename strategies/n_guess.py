
# Uses the optimal wordle strategy from:
# https://sonorouschocolate.com/notes/index.php/The_best_strategies_for_Wordle

# A generalization of the TwoGuess strategy, which supports any number of optimal guesses (though only 3, 4, or 5 make sense since
# the worst case is five guesses

# This implementation doesn't attempt to handle inconsistent clues, just returning a random word as a guess if there is an inconsistency.


from dataclasses import dataclass
import math
import random
import re
from tqdm import tqdm


answers = open("answers.txt").read().splitlines()

def get_optimal_guess(game_state):
    # find the next guess with a lazy regex
    clues = game_state[1::2]
    clue_patterns = [clue + " ([a-z]{5})" for clue in clues]
    pattern = "[\S\s]*?".join(clue_patterns)
    match = re.search(pattern, strategy)

    if match:
        return match.group(len(clues))
    else:
        return "crust"

guess_memo = {}
def compute_final_guess(game_state):

    memo_key = "".join(game_state)

    if memo_key in guess_memo:
        return guess_memo[memo_key]

    turns = len(game_state) // 2

    word_scores = []
    for word in answers:
        word_score = 5 * turns

        for k in range(turns):
            clue = game_state[2*k+1]
            guess = game_state[2*k]

            for i in range(5):
                cg = guess[i]
                cw = word[i]
                c = clue[i]
                if c == "G":
                    if cg != cw:
                        word_score -= 1
                elif c == "Y":
                    if cg == cw:
                        word_score -= 1
                    elif cg not in word:
                        word_score -= 1
                elif c == "B":
                    if cg in word:
                        word_score -= 1

        word_scores.append((word, word_score))
    word_scores.sort(key=lambda x: x[1], reverse=True)
    guess_memo[memo_key] = word_scores[0][0]
    return word_scores[0][0]


@dataclass
class NGuess:
    epsilon: float
    G: int

    def first_move(self):
        self.strategy = strategy
        self.strategy_lines = self.strategy.splitlines()    
        self.first_word = self.strategy_lines[0].split(" ")[0]
        self.answers = open("answers.txt").read().splitlines()
        self.turn = 1
        self.game_state = [self.first_word]
        return self.first_word, self.epsilon

    def next_move(self, guess, epsilon, clues):
        clue_map = {"c": "G", "i": "Y", ".": "B"}
        clue = "".join([clue_map[c] for c in clues])
        self.game_state.append(clue + str(self.turn))

        if self.turn + 1 < self.G:
            next_guess = get_optimal_guess(self.game_state)
            self.game_state.append(next_guess)
            self.turn += 1
            return next_guess, self.epsilon
        else:
            final_guess = compute_final_guess(self.game_state)
            return final_guess, 0


strategy = """
salet BBBBB1 courd BBBBB2 nymph BBBBY3 whiff GGGGG4
                                BGYYB3 pygmy GGGGG4
                                BYBBB3 fizzy GGGGG4
                                             YGBBG4 jiffy GGGGG5
                                BYBGY3 hippy GGGGG4
                                BYBYB3 piggy GGGGG4
                                BYGGB3 wimpy GGGGG4
                                GGGGG3
                                GYBBB3 ninny GGGGG4
                                YBYBB3 minim GGGGG4
                                YGBBB3 vying GGGGG4
                                YYBBB3 kinky GGGGG4
                                YYBBY3 whiny GGGGG4
                                YYBYB3 pinky GGGGG4
                   BBBBG2 vivid GGGGG3
                   BBBBY2 dingy GGBBG3 dizzy GGGGG4
                                GGGGG3
                                GYYYY3 dying GGGGG4
                                YGBBG3 biddy GGGGG4
                                YGBYG3 giddy GGGGG4
                                YGGBG3 windy GGGGG4
                   BBBGB2 myrrh GGGGG3
                   BBBYB2 baggy BBBBG3 privy GGGGG4
                                BBYBB3 wring GGGGG4
                                BBYBG3 grimy GGGGG4
                                GBBBB3 brink GGGGG4
                                GBBBG3 briny GGGGG4
                                GBYBB3 bring GGGGG4
                   BBBYG2 grind GGGGG3
                                YYYBG3 rigid GGGGG4
                   BBBYY2 drink GGGGG3
                   BBGYB2 gruff GGGGG3
                                YGGBB3 wrung GGGGG4
                   BBGYG2 druid GGGGG3
                   BBGYY2 drunk GGGGG3
                   BBYBB2 gimpy BBBBG3 funky BGGBG4 bunny GGGGG5
                                             BGGGG4 hunky GGGGG5
                                             GGBBG4 fuzzy GGGGG5
                                             GGGBG4 funny GGGGG5
                                             GGGGG4
                                BBBGG3 puppy GGGGG4
                                BBBYG3 puffy GGGGG4
                                BBGBG3 mummy GGGGG4
                                BBGGB3 humph GGGGG4
                                BBGGG3 jumpy GGGGG4
                                BYBBG3 unify GGGGG4
                                BYBYB3 unzip GGGGG4
                                GBBGG3 guppy GGGGG4
                                GBGBG3 gummy GGGGG4
                                YBBBG3 buggy GGGGG4
                                YYBBB3 fungi GGGGG4
                   BBYBG2 humid BYBGG3 undid GGGGG4
                                GGGGG3
                   BBYBY2 dumpy GGGBG3 dummy GGGGG4
                                GGGGG3
                                YGBBG3 buddy GGGGG4
                                YGBYG3 pudgy GGGGG4
                                YGYBG3 muddy GGGGG4
                   BBYGB2 furry BGBGB3 quirk GGGGG4
                                BGGGG3 hurry GGGGG4
                                GGGGG3
                   BBYYB2 murky BGYBG3 rugby GGGGG4
                                GGGGG3
                   BBYYY2 ruddy GGGGG3
                   BGBBB2 bongo BGBBB3 poppy GGGGG4
                                BGBBY3 woozy GGGGG4
                                BGBGB3 foggy GGGGG4
                                BGBYY3 goofy GGGGG4
                                BGYYB3 going GGGGG4
                                GGBBB3 bobby GGGGG4
                                GGBBY3 booby GGGBG4 boozy GGGGG5
                                             GGGGG4
                                GGGGG3
                                YGBBB3 hobby GGGGG4
                   BGBBY2 dowdy BGBGG3 goody BGGGG4 moody GGGGG5
                                             GGGGG4
                                BGGGG3 howdy GGGGG4
                                BGYGG3 woody GGGGG4
                                GGBBB3 doing GGGGG4
                                GGBYG3 dodgy GGGGG4
                                GGGBG3 downy GGGGG4
                                GGGGG3
                   BGBGB2 worry GGGGG3
                   BGBGY2 dowry GGGGG3
                   BGBYB2 horny BGGBB3 forgo GGGGG4
                                BGGYB3 moron GGGGG4
                                BGYBG3 roomy GGGGG4
                                BGYYB3 robin GGGGG4
                                GGGGG3
                                GGYYB3 honor GGGGG4
                                YGGBB3 morph GGGGG4
                   BGBYY2 rowdy GGGGG3
                                YGBYB3 donor GGGGG4
                                YGYGG3 wordy GGGGG4
                   BGGBB2 bough BGGYB3 young GGGGG4
                                GGGGG3
                   BGGBG2 bumph BYBBB3 found BGGGG4 wound GGGGG5
                                             GGGGG4
                                BYBBY3 hound GGGGG4
                                BYBYB3 pound GGGGG4
                                BYYBB3 mound GGGGG4
                                GYBBB3 bound GGGGG4
                   BGGBY2 dough GGGGG3
                   BGGGB2 mourn GGGGG3
                   BGGGG2 gourd GGGGG3
                   BGGYB2 rough GGGGG3
                   BGGYG2 round GGGGG3
                   BGYYB2 forum GGGGG3
                   BYBBB2 inbox BBBGB3 whoop GGGGG4
                                BGBYB3 known GGGGG4
                                BYBYB3 phony GGGGG4
                                GGGGG3
                                YBBYB3 hippo GGGGG4
                                YGBGB3 onion GGGGG4
                                YYBYB3 owing GGGGG4
                                YYYYB3 bingo GGGGG4
                   BYBBG2 ovoid GGGGG3
                   BYBBY2 dingo GGGGG3
                                YGBBY3 widow GGGGG4
                                YYBBY3 idiom GGGGG4
                   BYBGB2 ivory GGGGG3
                   BYBGG2 fjord GGGGG3
                   BYBGY2 hydro GGGGG3
                   BYBYB2 gimpy BBBBB3 brook BGGBB4 frown GGGGG5
                                             GGGBB4 brown GGGGG5
                                             GGGGG4
                                BBBYB3 proof GGGGG4
                                BBBYG3 proxy GGGGG4
                                BBYBB3 broom GGGGG4
                                BGYBB3 minor GGGGG4
                                BYBBB3 rhino GGGGG4
                                BYBBG3 irony GGGGG4
                                BYBYB3 prior GGGGG4
                                BYYYB3 primo GGGGG4
                                GBBBB3 grown GGGGG4
                                GBYBB3 groom GGGGG4
                                GYBBB3 groin GGGGG4
                                YBBBB3 wrong GGGGG4
                                YBBYB3 prong GGGGG4
                                YGBBB3 rigor BGGGG4 vigor GGGGG5
                                             GGGGG4
                   BYBYG2 brood BGGBG3 frond GGGGG4
                                GGGGG3
                   BYBYY2 droop GGGBB3 drown GGGGG4
                                GGGGG3
                   BYYBB2 gumbo BGGGG3 jumbo GGGGG4
                                BGYYY3 buxom GGGGG4
                                BYBBY3 union GGGGG4
                                BYYBY3 opium GGGGG4
                                GGGGG3
                   BYYYB2 furor BGBGG3 humor GGGGG4
                                BGGGG3 juror GGGGG4
                                BGYGG3 rumor GGGGG4
                                BYYYB3 group GGGGG4
                                GGGGG3
                   BYYYG2 proud GGGGG3
                   GBBBB2 cinch GGBYB3 civic GGGGG4
                                GGGGG3
                                GYBGY3 chick GGGGG4
                                GYGYB3 cynic GGGGG4
                   GBBGB2 chirp GGGGG3
                   GBBYB2 crick GGGBB3 crimp GGGGG4
                                GGGGG3
                   GBGBB2 chuck GGGBB3 chump GGGGG4
                                GGGBG3 chunk GGGGG4
                                GGGGG3
                   GBGGB2 churn GGGGG3
                   GBGYB2 crumb GGGGB3 crump GGGGG4
                                GGGGG3
                   GBYBB2 cubic GGBGB3 cumin GGGGG4
                                GGGGG3
                   GBYGB2 curry GGGGG3
                   GBYYB2 curvy GGGGG3
                   GGBBB2 comic GGBBY3 conch GGGGG4
                                GGBGG3 conic GGGGG4
                                GGGBB3 comfy GGGGG4
                                GGGGG3
                   GGBBY2 condo GGGGG3
                   GGBYB2 corny GGGGG3
                   GGGBB2 couch GGGBG3 cough GGGGG4
                                GGGGG3
                   GYBBB2 chock GGGGG3
                   GYBGG2 chord GGGGG3
                   GYBYB2 arson BGBGB3 crook GGGGG4
                                BGBYB3 crock GGGGG4
                                BGBYG3 crown GGGGG4
                                BGBYY3 crony GGGGG4
                                BYBYB3 choir GGGGG4
                   GYBYG2 crowd GGGGG3
                   GYYYB2 croup GGGGG3
                                GYYYB3 curio GGGGG4
                   YBBBB2 wimpy BGBBB3 finch GGGGG4
                                BGBYB3 pinch GGGGG4
                                BGBYG3 picky GGGGG4
                                BGGBB3 mimic GGGGG4
                                BYBBB3 icing GGGGG4
                                GGBBB3 winch GGGGG4
                                GYBBB3 which GGGGG4
                   YBBYB2 birch BYYGB3 prick GGGGG4
                                GGGGG3
                                GYYGB3 brick GGGGG4
                   YBYBB2 hempy BBBBB3 quick GGGGG4
                                BBBBG3 juicy GGGGG4
                                BBBYB3 pubic GGGGG4
                                BBYBG3 mucky GGGGG4
                                GBBBB3 hunch GGGGG4
                                YBBBB3 bunch GGGGG4
                                YBBYB3 punch GGGGG4
                                YBYBB3 munch GGGGG4
                   YBYBY2 duchy GGGGG3
                   YBYYB2 incur GGGGG3
                   YGBBB2 ionic BGBBY3 pooch GGGGG4
                                GGGGG3
                   YGBYB2 porch BGYYB3 rocky GGGGG4
                                GGGGG3
                   YGGBB2 pouch BGGGG3 vouch GGGGG4
                                GGGGG3
                   YYBBB2 knock GGGGG3
                   YYBGB2 micro GGGGG3
                   YYBYB2 frock GGGGG3
                   YYYYB2 occur GGGGG3
      BBBBG1 groin BBBBY2 uncut GGGGG3
                   BBBGY2 unfit GGGGG3
                   BBBYB2 twixt GGGGG3
                   BBBYY2 input GGGGG3
                   BBYBB2 doubt GGGGG3
                   BBYBY2 count BGGGG3 mount GGGGG4
                                BGYYG3 donut GGGGG4
                                GGGGG3
                   BBYGB2 vomit GGGGG3
                   BBYYB2 idiot GGGGG3
                                YBBGG3 pivot GGGGG4
                   BBYYY2 joint BGGGG3 point GGGGG4
                                GGGGG3
                   BGBBB2 crypt GGGGG3
                   BGBBY2 brunt GGGGG3
                   BGBGB2 fruit GGGGG3
                   BGBYB2 drift GGGGG3
                   BGBYY2 print GGGGG3
                   BGGBB2 trout GGGGG3
                   BGGBY2 front GGGGG3
                   BGGGB2 droit GGGGG3
                   BGYGB2 orbit GGGGG3
                   BYBBY2 burnt GGGGG3
                   BYYBB2 court BGBYG3 robot GGGGG4
                                GGGGG3
                   GGBBY2 grunt GGGGG3
                   GGGBB2 grout GGGGG3
                   YBBGB2 digit GGGGG3
                   YBBYB2 awful BBBBB3 might BGGGG4 tight GGGGG5
                                             GGGGG4
                                BBYBB3 fight GGGGG4
                                BYBBB3 wight GGGGG4
                   YBBYY2 night GGGGG3
                   YBYBB2 ought GGGGG3
                   YBYYB2 bigot GGGGG3
                   YBYYY2 ingot GGGGG3
                   YYBYB2 right GGGGG3
      BBBBY1 north BBBGB2 batik BBGBB3 putty GGGGG4
                                BBGYB3 ditty BGGGG4 witty GGGGG5
                                             GGGGG4
                                BBGYY3 kitty GGGGG4
                                BBYYB3 fifty GGGGG4
                                GBGYB3 bitty GGGGG4
                   BBBGG2 fifth BGBGG3 width GGGGG4
                                GGGGG3
                   BBBYB2 timid GGGGG3
                   BBBYG2 biped BBBBB3 hutch GGGGG4
                                BBBBY3 dutch GGGGG4
                                BGBBB3 hitch BGGGG4 witch GGGGG5
                                             GGGGG4
                                BGBBY3 ditch GGGGG4
                                BGYBB3 pitch GGGGG4
                                BYBBB3 thigh GGGGG4
                                GBBBB3 butch GGGGG4
                   BBBYY2 pithy BBYYB3 thumb GGGGG4
                                BYYGG3 itchy GGGGG4
                                BYYYB3 thick GGGGG4
                                GGGGG3
                                YBYYB3 thump GGGGG4
                   BBGGB2 dirty GGGGG3
                   BBGGG2 album BBBBB3 girth GGGGG4
                                BBBBY3 mirth GGGGG4
                                BBYBB3 birth GGGGG4
                   BBGYY2 thrum GGGGG3
                   BBYGB2 fritz GGGGG3
                   BBYGG2 truth GGGGG3
                   BBYYB2 trick GGBBB3 trump GGGGG4
                                GGBGG3 truck GGGGG4
                                GGGGG3
                   BBYYY2 third GGGGG3
                   BGBGB2 booty BGBGG3 pouty GGGGG4
                                BGYGB3 motto GGGGG4
                                GGGGG3
                   BGBGG2 album BBBBB3 tooth GGGGG4
                                BBBYB3 youth GGGGG4
                                BBBYY3 mouth GGGGG4
                                BBYBB3 booth GGGGG4
                   BGBYB2 topic GGBBB3 toddy GGGGG4
                                GGBGG3 toxic GGGGG4
                                GGGGG3
                                YGBGB3 motif GGGGG4
                   BGBYG2 botch BGYBG3 tough GGGGG4
                                BGYGG3 touch GGGGG4
                                GGGGG3
                   BGGGB2 forty GGGGG3
                   BGGGG2 forth BGGGG3 worth GGGGG4
                                GGGGG3
                   BGGYG2 torch GGGGG3
                   BGYYB2 motor BGGGG3 rotor GGGGG4
                                GGGGG3
                   BYBGB2 ditto GGGGG3
                   BYBGG2 quoth GGGGG3
                   BYBGY2 photo GGGGG3
                   BYBYB2 outdo GBGBB3 optic GGGGG4
                                GGGBG3 outgo GGGGG4
                                GGGGG3
                   BYGYB2 turbo GGGGG3
                   BYGYY2 throb GGGGB3 throw GGGGG4
                                GGGGG3
                   BYYGG2 broth BGGGG3 froth GGGGG4
                                GGGGG3
                   BYYYB2 tumor GBBGY3 troop GGGGG4
                                GGBGG3 tutor GGGGG4
                                GGGGG3
                   GBBGB2 nutty GGGGG3
                   GBBGG2 ninth GGGGG3
                   GGBYG2 notch GGGGG3
                   GGGGG2
                   YBBGB2 minty BYYGG3 unity GGGGG4
                                GGGGG3
                   YBBYB2 tunic GBYYB3 tying GGGGG4
                                GGGGG3
                   YBBYY2 thing GGGGB3 think GGGGG4
                                GGGGG3
                   YBYYB2 trunk GGGGG3
                   YGBGG2 month GGGGG3
                   YGBYB2 tonic GGGGG3
                                GGYGB3 toxin GGGGG4
                   YYBGB2 junto BBGGG3 pinto GGGGG4
                                GGGGG3
                   YYBYY2 thong GGGGG3
                   YYYYB2 intro GGGGG3
                   YYYYY2 thorn GGGGG3
      BBBGB1 rownd BBBBB2 bicep BBGGB3 emcee GGGGG4
                                BBYGB3 cheek GGGGG4
                                BYYGB3 chief GGGGG4
                                GGGGG3
                   BBBBG2 embed GGGGG3
                   BBBBY2 dicey GGGGG3
                   BBBYB2 buggy BBBBB3 vixen GGGGG4
                                BBBBG3 piney GGGGG4
                                BBBBY3 hymen GGGGG4
                                BBYBB3 given GGGGG4
                                BGBBB3 queen GGGGG4
                   BBBYG2 kneed BGBGG3 unfed GGGGG4
                                GGGGG3
                   BBBYY2 index GGGGG3
                   BBGYG2 unwed GGGGG3
                   BBYYY2 widen GGGGG3
                   BGBBB2 covey BGBGG3 gooey GGGGG4
                                GGGGG3
                   BGBBY2 dopey GGGGG3
                                YGBGB3 modem GGGGG4
                   BGBYB2 balmy BBBBB3 coven GGGGG4
                                BBBBG3 honey GGGGG4
                                BBBYG3 money GGGGG4
                                GBBBG3 boney GGGGG4
                   BGBYY2 dozen GGGGG3
                   BGYYB2 evoke YBYBB3 women GGGGG4
                                YBYYB3 woken GGGGG4
                                YYYBB3 woven GGGGG4
                   BYBBY2 video GGGGG3
                   GBBBB2 riper GBBGG3 refer GGGGG4
                                GBGGB3 rupee GGGGG4
                                GGBGG3 river GGGGG4
                                GGGGG3
                   GBBBY2 rider GBGGG3 ruder GGGGG4
                                GGGGG3
                   GBBYB2 ripen GGGGG3
                   GBYYB2 renew GGGGG3
                   GGBBB2 roger GGBGG3 rover GGGGG4
                                GGGGG3
                   GGBBY2 rodeo GGGGG3
                   GGGBB2 rower GGGGG3
                   YBBBB2 pubic BBBBB3 fever GGGGG4
                                             GYBGG4 freer GGGGG5
                                BBBBY3 cheer GBGGY4 creek GGGGG5
                                             GGGGG4
                                BBBYB3 fixer BGBGG4 giver GGGGG5
                                             GGGGG4
                                             YYBGY4 grief GGGGG5
                                BBBYY3 crier GGGGG4
                                BBGBB3 ember GGGGG4
                                BBGBY3 cyber GGGGG4
                                BBGYB3 fiber GGGGG4
                                BBYYB3 brief GGGGG4
                                BGBBB3 queer GGGGG4
                                BGYBB3 buyer GGGGG4
                                GBBYB3 piper GGGGG4
                                GGBBB3 puree GGGGB4 purer GGGGG5
                                             GGGGG4
                                YBBBB3 hyper GGGGG4
                                YBBBY3 creep GGGGG4
                                YBBYB3 viper GGGGG4
                                YYBBB3 upper GGGGG4
                   YBBBG2 bicep BBBGB3 freed BGGGG4 greed GGGGG5
                                             GGGGG4
                                BBYGB3 creed GGGGG4
                                BYBGB3 dried BGGGG4 fried GGGGG5
                                             GGGGG4
                                BYBGY3 pried GGGGG4
                                BYYGB3 cried GGGGG4
                                GBBGB3 breed GGGGG4
                   YBBBY2 drier GBBGG3 defer GGGGG4
                                GBYGG3 diver GGGGG4
                                GGBGG3 dryer GGGGG4
                                GGGGG3
                                YBBGG3 udder GGGGG4
                                YBYGG3 cider GGGGG4
                   YBBYB2 finer BBYGG3 never GGGGG4
                                BBYGY3 green BGGGG4 preen GGGGG5
                                             GGGGG4
                                BGGGG3 miner GGGGG4
                                BGYGG3 nicer GGGGG4
                                BYGGG3 inner GGGGG4
                                GGGGG3
                                YYYGG3 infer GGGGG4
                   YBBYY2 diner GGGGG3
                                YBYGG3 under GGGGG4
                   YBGBB2 fewer GGGGG3
                   YBGYB2 newer GGGGG3
                   YBYBY2 wider GGGGG3
                   YGBBB2 chevy BBYBB3 joker BGBGG4 boxer GGGGG5
                                             BGGGG4 poker GGGGG5
                                             GGGGG4
                                BBYBY3 foyer GGGGG4
                                BBYYB3 mover GGGGG4
                                BYYBB3 homer GGGGG4
                                BYYYB3 hover GGGGG4
                                GBYBB3 corer GGGGG4
                                GBYYB3 cover GGGGG4
                   YGBYB2 goner GGGGG3
                   YGGBB2 ample BBBBY3 cower GGGGG4
                                BBYBY3 power GGGGG4
                                BYBBY3 mower GGGGG4
                   YGYBB2 wooer GGGGG3
                   YYBBB2 offer GGGGG3
                   YYBBY2 odder GBGGG3 order GGGGG4
                                GGGGG3
                   YYYYB2 owner GGGGG3
      BBBGG1 cerne BGBBY2 beget GGGGG3
                   BGBYY2 tenet GGGGG3
                   BGGBY2 beret GGGGG3
                   BYBBB2 duvet BGBGG3 quiet GGGGG4
                                GGGGG3
                   BYBBY2 tweet GGGGG3
                   BYBYB2 unmet GGGGG3
                   BYGBY2 egret GGGGG3
                   BYYBB2 rivet GGGGG3
                   BYYBY2 greet GGGGG3
                   GYBBB2 comet GGBGG3 covet GGGGG4
                                GGGGG3
                   YYBBB2 octet GGGGG3
      BBBGY1 mohur BBBBB2 tepee GGGGG3
                                GYBGB3 tweed GGGGG4
                   BBBBG2 deter BBGGG3 inter GGGGG4
                                BBYGG3 tiger GGGGG4
                                BYGGG3 enter GGGGG4
                                GGGGG3
                   BBBBY2 tried GGGGG3
                   BBBYG2 truer GBYGG3 tuber GGGGG4
                                GGGGG3
                                YBYGG3 utter GGGGG4
                   BBGBG2 ether GGGGG3
                   BBYBB2 thief GGGGG3
                   BBYBY2 three GGGGB3 threw GGGGG4
                                GGGGG3
                   BGBBB2 token GGGGG3
                   BGBBG2 tower GGGGG3
                                YGBGG3 voter GGGGG4
                   BYBBB2 often GGGGG3
                   BYBBG2 otter GGGGG3
                   BYBYG2 outer GGGGG3
                   BYGBG2 other GGGGG3
                   GBBBG2 meter GGGGG3
                   YBBBG2 timer GGGGG3
                   YGBBB2 totem GGGGG3
      BBBYB1 drone BBBBG2 ficus BBBGB3 queue GGGGG4
                                BGBBB3 pixie GGGGG4
                                BGBGB3 pique GGGGG4
                                BGYBB3 piece GGGGG4
                                BYBGB3 imbue GGGGG4
                                BYYBB3 chime GGGGG4
                                BYYYB3 juice GGGGG4
                                GBBBB3 femme GGGGG4
                                GBBGB3 fugue GGGGG4
                   BBBBY2 beech BBGGY3 check GGGGG4
                                BGBBG3 weigh GGGGG4
                                BGGBB3 geeky GGGGG4
                                BYBBB3 equip GGGGG4
                                GGGBB3 beefy GGGGG4
                                GGGGG3
                   BBBGG2 penne BBBGG3 whine GGGGG4
                                GGGGG3
                   BBBGY2 eking GBGGG3 eying GGGGG4
                                GGGGG3
                                YBBGB3 penny GGGGG4
                                YBGGG3 being GGGGG4
                   BBBYG2 finch BBGBB3 venue GGGGG4
                                BBGGB3 pence GGGGG4
                                BBGGY3 hence GGGGG4
                                BGGBB3 binge GGGGG4
                                BGGBY3 hinge GGGGG4
                                BGGGB3 mince BGGGG4 wince GGGGG5
                                             GGGGG4
                                BGYGB3 niece GGGGG4
                                BGYYY3 niche GGGGG4
                                BYGBB3 genie GGGGG4
                                GBGGB3 fence GGGGG4
                                YYYBB3 knife GGGGG4
                   BBBYY2 begin BGBBY3 wench GGGGG4
                                BGYYG3 feign GGGGG4
                                BGYYY3 neigh GGGGG4
                                BYBBY3 enemy GGGGG4
                                BYBYY3 ennui GGGGG4
                                GGBBY3 bench GGGGG4
                                GGGBG3 begun GGGGG4
                                GGGGG3
                   BBGBG2 basic BBBBB3 evoke GGGGG4
                                BBBBY3 choke GGGGG4
                                GBBBB3 booze GGGGG4
                                GBBYB3 biome GGGGG4
                   BBGBY2 epoch GGGBB3 epoxy GGGGG4
                                GGGGG3
                   BBGGG2 ozone BBGGG3 phone GGGGG4
                                GGGGG3
                   BBGGY2 ebony GGGGG3
                   BBGYG2 gnome GGGGG3
                   BBYBG2 coupe BGBBG3 movie GGGGG4
                                BGGBG3 gouge GGGGG4
                                BGYBG3 vogue GGGGG4
                                GGGGG3
                                YGBBG3 voice GGGGG4
                   BBYBY2 gecko GGGGG3
                   BBYGG2 opine GBGGG3 ovine GGGGG4
                                GGGGG3
                   BBYYG2 ounce GGGGG3
                   BBYYY2 enjoy GGBGG3 envoy GGGGG4
                                GGGGG3
                                YYBGB3 venom GGGGG4
                   BGBBG2 campi BBBBY3 bribe GGGGG4
                                BBBGY3 gripe GGGGG4
                                BBBYY3 prize GGGGG4
                                BBYBY3 grime GGGGG4
                                BBYYY3 prime GGGGG4
                                GBBGB3 crepe GGGGG4
                                GBYBB3 creme GGGGG4
                                GBYBY3 crime GGGGG4
                                YBBYY3 price GGGGG4
                   BGBBY2 wreck GGGGG3
                   BGBGG2 brine BGBGG3 prune GGGGG4
                                BGGGG3 urine GGGGG4
                                GGGGG3
                   BGGBG2 probe BGGBG3 froze BGGBG4 grove GGGGG5
                                             GGGGG4
                                BGGYG3 broke GGGGG4
                                GGGBG3 prove GGGGG4
                                GGGGG3
                                YGGBG3 grope GGGGG4
                   BGGGG2 crone BGGGG3 prone GGGGG4
                                GGGGG3
                   BGYBY2 error GGGGG3
                   BYBBG2 reive GBBBG3 rhyme GGGGG4
                                GGBYG3 revue GGGGG4
                                YBBBG3 purge GGGGG4
                                YBBGG3 curve GGGGG4
                                YBYBG3 fibre GGGGG4
                                YGBBG3 merge GGGGG4
                                YGBGG3 verve GGGGG4
                                YGBYG3 verge GGGGG4
                                YGYBG3 eerie GGGGG4
                                YYBBG3 where GGGGG4
                   BYBBY2 murry BBBGG3 every BBGGG4 fiery GGGGG5
                                             GGGGG4
                                BBGBB3 perch GGGGG4
                                BBGBG3 jerky BGGGG4 perky GGGGG5
                                             GGGGG4
                                BBGGG3 berry BGGGG4 ferry GGGGG5
                                             GGGGG4
                                BGBGG3 query GGGGG4
                                BYYYB3 recur GGGGG4
                                GBGBG3 mercy GGGGG4
                                GBGGG3 merry GGGGG4
                                YYYBB3 femur GGGGG4
                   BYBYG2 genre BGYYG3 nerve GGGGG4
                                GGGGG3
                   BYBYY2 reign GGBBG3 rerun GGGGG4
                                GGGGG3
                   BYGBG2 chore GGGGG3
                   BYYBG2 forge BGGGG3 gorge GGGGG4
                                BGYGG3 rouge GGGGG4
                                BGYYG3 rogue GGGGG4
                                BYYBG3 ombre GGGGG4
                                GGGBG3 force GGGGG4
                                GGGGG3
                   BYYGG2 borne GGGGG3
                   BYYYY2 heron GGGGG3
                   GBBBG2 deuce GGGGG3
                   GBBBY2 debug GGGGG3
                   GBBYG2 dunce GGGGG3
                   GBBYY2 deign GGGGG3
                                GGYBY3 denim GGGGG4
                   GBGBG2 diode GGGGG3
                   GBYBG2 dodge GGGGG3
                   GBYBY2 decoy GGGGG3
                   GBYYY2 demon GGGGG3
                   GGBBG2 drive GGGGG3
                   GGGBG2 drove GGGGG3
                   GGGGG2
                   GYBBG2 dirge GGGGG3
                   GYBBY2 decry GGBYB3 demur GGGGG4
                                GGBYG3 derby GGGGG4
                                GGGGG3
                   GYYBY2 decor GGGGG3
                   YBBBG2 whiff BBBBB3 budge BGGGG4 judge GGGGG5
                                             GGGGG4
                                BBBYB3 fudge GGGGG4
                                BBGBB3 guide GGGGG4
                                BBYBB3 midge GGGGG4
                                BGGBB3 chide GGGGG4
                                BYBBB3 hedge GGGGG4
                                GBBBB3 wedge GGGGG4
                   YBBBY2 edify GGGGG3
                                YYBBG3 weedy GGGGG4
                                YYYBB3 medic GGGGG4
                   YBBGY2 fiend GGGGG3
                   YBBYG2 nudge GGGGG3
                                YYGBG3 undue GGGGG4
                   YBBYY2 needy GGGGG3
                   YBYBG2 oxide GGGGG3
                   YBYYY2 endow GGGGG3
                   YGBBG2 pride BGBGG3 crude GGGGG4
                                BGGGG3 bride GGGGG4
                                GGBGG3 prude GGGGG4
                                GGGGG3
                   YGGBG2 erode GGGGG3
                   YGYBY2 credo GGGGG3
                   YYBBG2 ridge GGGGG3
                   YYBBY2 reedy GGGGG3
                                YGBYB3 weird GGGGG4
                   YYBYY2 nerdy GGGGG3
                   YYYBG2 horde GGGGG3
      BBBYG1 curio BBBBB2 event BBGBG3 theft GGGGG4
                                GGGGG3
                   BBBBY2 depot GGGGG3
                   BBBGB2 befit GGGGG3
                                YGBGG3 debit GGGGG4
                   BBBYB2 eight GGGGG3
                                YYBBG3 inept GGGGG4
                   BBGGB2 merit GGGGG3
                   BBYBB2 exert GGGGG3
                   BBYBY2 overt GGGGG3
                   BBYGB2 refit GGBGG3 remit GGGGG4
                                GGGGG3
                   BBYYB2 inert GGGGG3
                   BYBBB2 debut GGGGG3
                   BYYBB2 erupt GGGGG3
                                YYYBG3 rebut GGGGG4
                   GBYBB2 crept GGGGG3
                   YBBBB2 eject GGGGG3
                   YBBYB2 edict GBGGG3 evict GGGGG4
                                GGGGG3
                   YBYBB2 erect GGGGG3
                   YYYBB2 recut GGGGG3
      BBBYY1 trite BBBGG2 chute BBYGG3 quote GGGGG4
                                GGGGG3
                   BBBGY2 depth BGBGY3 hefty GGGGG4
                                BYGGB3 empty GGGGG4
                                GGGGG3
                   BBGGG2 quite BBGGG3 white GGGGG4
                                BYGGG3 unite GGGGG4
                                GGGGG3
                   BBGGY2 deity GGGGG3
                   BBYGY2 piety GGGGG3
                   BGBGG2 brute BGBGG3 wrote GGGGG4
                                GGGGG3
                   BGGGG2 write GGGGG3
                   BYBGG2 forte BGYGG3 route GGGGG4
                                GGGGG3
                   BYBGY2 berth GGGGG3
                   GBBBG2 theme GGBGG3 thyme GGGGG4
                                GGGGG3
                   GBBBY2 teddy GGBBB3 tempo GGGGG4
                                GGGGG3
                   GBBGY2 teeth GGBGG3 tenth GGGGG4
                                GGGGG3
                   GBGBG2 twice GGGBG3 twine GGGGG4
                                GGGGG3
                   GBYBY2 tepid GGGGG3
                   GBYYG2 tithe GGGGG3
                   GGBBG2 trope GGBBG3 truce GGGGG4
                                GGGBG3 trove GGGGG4
                                GGGGG3
                   GGBBY2 trend GGGGG3
                   GGGBG2 aback BBBBB3 tripe GGGGG4
                                BBBGB3 trice GGGGG4
                                BYBBB3 tribe GGGGG4
                   GGGGG2
                   GYBBG2 there GGGGG3
                   GYBBY2 tenor GGGGG3
                   GYYBY2 their GGGGG3
                   YBBBG2 etude GGGGG3
                   YBBBY2 detox BGGBB3 fetch GGGGG4
                                GGGGG3
                   YBBGG2 butte GGGGG3
                   YBBGY2 jetty BGGGG3 petty GGGGG4
                                GGGGG3
                   YBYBG2 cutie BYGGG3 untie GGGGG4
                                GGGGG3
                   YBYBY2 ethic GGGGG3
                                YYBGB3 fetid GGGGG4
                   YYBBY2 metro BGGGB3 retry GGGGG4
                                BGGGG3 retro GGGGG4
                                BGGYB3 retch GGGGG4
                                BYGGB3 entry GGGGG4
                                GGGGG3
      BBGBB1 fugly BBBGG2 howdy BBBBG3 billy GGGGG4
                                BBBYG3 dilly GGGGG4
                                BBYBG3 willy GGGGG4
                                BGBBG3 jolly GGGGG4
                                BGBYG3 dolly GGGGG4
                                GBBBG3 hilly GGGGG4
                                GGBBG3 holly GGGGG4
                   BBBYB2 colon GGGGB3 color GGGGG4
                                GGGGG3
                   BBBYG2 milky GBGBG3 moldy GGGGG4
                                GGGGG3
                   BBBYY2 nylon BYGYB3 polyp GGGGG4
                                GGGGG3
                   BBYGG2 golly GGGGG3
                   BBYYB2 igloo GGGGG3
                   BGBGG2 bully BGGGG3 dully GGGGG4
                                GGGGG3
                   BGBYB2 mulch GGGGG3
                   BGBYG2 bulky BGGBG3 pulpy GGGGG4
                                GGGGG3
                   BGYGG2 gully GGGGG3
                   BGYYB2 gulch GGGGG3
                   GBBGG2 filly GBGGG3 folly GGGGG4
                                GGGGG3
                   GBBYB2 folio GGGGG3
                   GBBYG2 filmy GGGGG3
                   GGBGG2 fully GGGGG3
      BBGBG1 pilot BYGBG2 unlit GGGGG3
                   GGGGG2
      BBGBY1 filth BYGYB2 tulip GGGGG3
                   GGGGG2
      BBGGB1 afire BBBBG2 melee GGGGG3
                   BBBBY2 golem GGGGG3
                   BBBYY2 ruler GGGGG3
                   BBYYY2 idler GGGGG3
                   BYYYY2 filer GGGGG3
      BBGGG1 filet BYGGG2 inlet GGGGG3
                   GGGGG2
      BBGYB1 himbo BBBBB2 delve BGGBB3 jelly GGGGG4
                                GGGGG3
                   BBBBG2 cello GGGGG3
                   BBBBY2 felon GGGGG3
                   BBBYB2 belle GBGBG3 bulge GGGGG4
                                GGGGB3 belly GGGGG4
                                GGGGG3
                   BBBYY2 below GGGGG3
                   BBYBY2 melon GGGGG3
                   BGBYB2 bilge GGGGG3
                   BYBBB2 relic GGGGG3
                   BYBYB2 belie GGGGG3
                   GBBBG2 hello GGGGG3
                   GYBBB2 helix GGGGG3
                   YBBBB2 welch GGGGG3
                   YBBYB2 belch GGGGG3
      BBGYY1 tilde GBGBG2 tulle GGGGG3
                   GGGGG2
      BBYBB1 courd BBBBB2 fling BGBBY3 glyph GGGGG4
                                BGGBB3 blimp GGGGG4
                                BGGGB3 blink GGGGG4
                                BYBBB3 lymph GGGGG4
                                BYGGG3 lying GGGGG4
                                BYYBB3 imply GGGGG4
                                BYYBY3 vigil GGGGG4
                                BYYYB3 vinyl GGGGG4
                                GGGGG3
                   BBBBG2 lipid GGBGG3 livid GGGGG4
                                GGGGG3
                                YYBBG3 blind GGGGG4
                   BBBBY2 dimly GGGGG3
                                YYBGY3 idyll GGGGG4
                   BBBGB2 whirl GGGGG3
                   BBBYB2 eking BBBBB3 wryly GGGGG4
                                BBGBB3 frill GGGGG4
                                BBGBY3 grill GGGGG4
                                BBYBY3 girly GGGGG4
                                BYGBB3 krill GGGGG4
                   BBBYY2 drill GGBGB3 dryly GGGGG4
                                GGGGG3
                   BBGBB2 flung BGGBB3 plumb GGGGB4 plump GGGGG5
                                             GGGGG4
                                BGGGB3 plunk GGGGG4
                                GGGBB3 fluff GGGGG4
                                GGGGB3 flunk GGGGG4
                                GGGGG3
                                YGGBB3 bluff GGGGG4
                   BBGBG2 fluid GGGGG3
                   BBGGB2 blurb GGGGG3
                   BBYBB2 lumpy GGGGG3
                                YGBBB3 quill GGGGG4
                                YGBYB3 pupil GGGGG4
                   BBYBG2 build BGGGG3 guild GGGGG4
                                GGGGG3
                   BBYYB2 burly GGGGG3
                   BBYYG2 lurid GGGGG3
                   BGBBB2 wooly BGBGG3 nobly GGGGG4
                                BGBYB3 login GGGGG4
                                BGBYG3 lobby GGGGG4
                                BGGYG3 loopy GGGGG4
                                GGGGG3
                                YGBGG3 lowly GGGGG4
                   BGBBY2 godly GGGGG3
                   BGBGB2 lorry GGGGG3
                   BGBYG2 world GGGGG3
                   BGGBG2 would GGGGG3
                   BGYBB2 mogul GGGGG3
                   BYBBB2 bloom BGGBB3 flown GGGGG4
                                BGGGG3 gloom GGGGG4
                                BYGBB3 knoll GGGGG4
                                BYYBB3 lingo GGGGG4
                                GGGBB3 blown GGGGG4
                                GGGGG3
                                YYYBY3 limbo GGGGG4
                   BYBBG2 blond BGGBG3 flood GGGGG4
                                GGGBG3 blood GGGGG4
                                GGGGG3
                   BYBBY2 oddly GGGGG3
                   BYBGB2 glory GGGGG3
                   BYBYB2 growl BGGBG3 broil GGGGG4
                                BGGGG3 prowl GGGGG4
                                BYGBY3 floor GGGGG4
                                GGGGG3
                   BYBYY2 droll GGGBG3 drool GGGGG4
                                GGGGG3
                   BYYBB2 ghoul GGGGG3
                   BYYYB2 flour GGGGG3
                   GBBBB2 blink BGGBB3 cliff GGGGG4
                                BGGBG3 click GGGGG4
                                BGGGB3 cling GGGGG4
                                BGGGG3 clink GGGGG4
                                BYGBB3 chili GGGGB4 chill GGGGG5
                                             GGGGG4
                                BYYBB3 civil GGGGG4
                                YGGBB3 climb GGGGG4
                   GBBBG2 child GGGGG3
                   GBGBB2 admin BBBBB3 cluck GGGGG4
                                BBBBY3 clung GGGGG4
                                BBYBB3 clump GGGGG4
                   GBYYB2 curly GGGGG3
                   GGBBB2 coyly GGGGG3
                   GGGBG2 could GGGGG3
                   GYBBB2 clock GGGBB3 clown GGGGG4
                                GGGGG3
                   GYYBG2 cloud GGGGG3
                   YBBBB2 flick BYBGB3 lynch GGGGG4
                                BYGYB3 icily GGGGG4
                                GGGGG3
                   YBBYB2 lyric GGGGG3
                   YBGBB2 pluck GGGGG3
                   YBYBB2 lucky GGGGG3
                                GGYBB3 lunch GGGGG4
                   YBYBG2 lucid GGGGG3
                   YBYYB2 lurch GGGGG3
                   YGBBB2 logic GGGGG3
                   YYBBB2 block BGGGG3 flock GGGGG4
                                GGGGG3
      BBYBG1 clung BGBBB2 flirt GGGGG3
                   BGBGB2 flint GGGGG3
                   BGBGY2 glint GGGGG3
                   BGGBB2 blurt GGGGG3
                   BGGGB2 blunt GGGGG3
                   BGYBB2 flout GGGGG3
                   BYBBB2 limit GGGGG3
                   BYBBY2 light GGGGG3
                   BYGBB2 moult GGGGG3
                   BYYBB2 built BGGGG3 quilt GGGGG4
                                GGGGG3
                   BYYBY2 guilt GGGGG3
                   GGYBB2 clout GGGGG3
      BBYBY1 troll GGBGB2 truly GGGGG3
                   GGGGG2
                   GYBBG2 twirl GGGGG3
                   YBBBG2 until GGGGG3
                   YBBYB2 blitz GGGGG3
                   YBGYB2 cloth GGGGG3
                   YBYGB2 hotly GGGGG3
                   YBYYB2 lofty GGGGG3
      BBYGB1 bevor BGBBB2 jewel GGGGG3
                   BGBBG2 leper GGGGG3
                   BGBBY2 repel GGGGG3
                   BGGBB2 level GGGGG3
                   BGGBG2 lever GGGGG3
                   BGGBY2 revel GGGGG3
                   BYBBB2 picky BBBBB3 lumen GGGGG4
                                             YBBGB4 wheel GGGGG5
                                BBBYB3 kneel GGGGG4
                                BBGBB3 excel GGGGG4
                                BBYBB3 clued GGGGG4
                                BGBBB3 linen GGGGG4
                                BGBYB3 liken GGGGG4
                                GGBBB3 pixel GGGGG4
                                GYBBB3 plied GGGGG4
                                YBBBB3 expel GGGGG4
                                YYBBB3 impel GGGGG4
                   BYBBG2 chief BBBGB3 elder GGGGG4
                                BBBGY3 flyer GGGGG4
                                BBGGB3 plier GGGGG4
                                BBGGY3 flier GGGGG4
                                BBYGB3 liner GGGGG4
                                YBBGB3 ulcer GGGGG4
                   BYBBY2 cruel BGGGG3 gruel GGGGG4
                                GGGGG3
                   BYBYB2 dowel GGGGG3
                                YGBGG3 model GGGGG4
                                YYBGY3 olden GGGGG4
                   BYBYG2 lower GGGGG3
                                YYBGG3 older GGGGG4
                   BYGBG2 liver GGGGG3
                   BYGYB2 hovel BGGGG3 novel GGGGG4
                                GGGGG3
                   BYGYG2 lover GGGGG3
                   BYYYB2 vowel GGGGG3
                   GGBBB2 bezel GGGGG3
                   GGGBB2 bevel GGGGG3
                   GYBBB2 bleed GGGGB3 bleep GGGGG4
                                GGGGG3
                   GYBBG2 bluer GGGGG3
                   GYBYB2 bowel GGGGG3
                   YGBBY2 rebel GGGGG3
                   YYBBB2 libel GGGGG3
      BBYGG1 fleet GGGGG2
      BBYGY1 hotel BBGGG2 betel GGGGG3
                   BGGGG2 motel GGGGG3
                   BGYGG2 towel GGGGG3
                   GGGGG2
      BBYYB1 deice BBBBG2 bloke BGBBG3 flume BGGGG4 plume GGGGG5
                                             GGGGG4
                                BGBGG3 fluke GGGGG4
                                BGGBG3 glove GGGGG4
                                BYBBG3 lunge GGGGG4
                                BYGBG3 whole GGGGG4
                                GGGGG3
                                GYBBG3 bugle GGGGG4
                                GYYBG3 boule GGGGG4
                                YGGBG3 globe GGGGG4
                                YYYBG3 noble GGGGG4
                   BBBYG2 clone GGGBG3 clove GGGGG4
                                GGGGG3
                                GYBBG3 cycle GGGGG4
                                YYBYG3 uncle GGGGG4
                   BBGBG2 guile BBGGG3 while GGGGG4
                                BBGYG3 olive GGGGG4
                                GGGGG3
                   BBYBG2 bible BGBGG3 rifle GGGGG4
                                GGGGG3
                   BGBBB2 lemon GGBBB3 leggy GGGGG4
                                GGGBB3 lemur GGGGG4
                                GGGGG3
                                YGBBB3 reply GGGGG4
                                YGBBY3 newly GGGGG4
                   BGBBY2 leery GGGGG3
                   BGBGY2 leech GGGGG3
                   BGYBB2 peril GGGGG3
                   BYBBB2 elbow GGGGG3
                                YYBBB3 quell GGGGG4
                                YYBBY3 whelp GGGGG4
                   BYBBG2 elope GGGGG3
                   BYBBY2 elegy GGGGG3
                   BYBGB2 fleck GGGGG3
                   BYBYB2 clerk GGGGG3
                   BYGBG2 exile GGGGG3
                   BYYBB2 elfin GGGGG3
                   BYYBG2 liege GGGGG3
                   GGYBB2 devil GGGGG3
                   GYBBB2 dwell GGGGG3
                   YBBBG2 lodge GGGGG3
                   YBGBG2 glide GGGGG3
                   YGBBG2 ledge GGGGG3
                   YYBBB2 blend GGGGG3
                   YYBBG2 elude GGGGG3
                   YYGBG2 elide GGGGG3
                   YYYBB2 awful BBBBY3 yield GGGGG4
                                BBYBY3 field GGGGG4
                                BYBBY3 wield GGGGG4
      BBYYG1 bleed BGGBB2 cleft GGGGG3
                   BGGYB2 elect GGGGG3
                   BYGBB2 knelt GGGGG3
                   BYGBY2 dwelt GGGGG3
                   BYYBB2 exult GGGGG3
      BBYYY1 title BBGYY2 extol GGGGG3
                   BGGYG2 lithe GGGGG3
                   GGGGG2
                   YBBYG2 flute GGGGG3
                   YBBYY2 lefty GGGGG3
                   YYBGG2 utile GGGGG3
                   YYBYG2 elite GGGGG3
      BGBBB1 corny BBBBB2 gamma BGBBB3 vapid GGGGG4
                                BGBBG3 kappa GGGGG4
                                BGGGG3 mamma GGGGG4
                                BGYBG3 mafia GGGGG4
                                BGYYB3 maxim GGGGG4
                                BGYYY3 madam GGGGG4
                                GGGGG3
                                YGYGG3 magma GGGGG4
                   BBBBG2 pudgy BBBBG3 jazzy BGBBG4 mammy GGGGG5
                                             GGGGG4
                                BBBGG3 baggy GGGGG4
                                BBBYG3 gawky GGGGG4
                                BBGBG3 daddy GGGGG4
                                BBYBG3 bawdy GGGGG4
                                BYYYG3 gaudy GGGGG4
                                GBGBG3 paddy GGGGG4
                                YBBBG3 happy GGGGG4
                   BBBBY2 kayak GGGGG3
                   BBBGB2 fauna GGGGG3
                   BBBGG2 fanny BGGGG3 nanny GGGGG4
                                GGGGG3
                   BBBYB2 manga BGYYY3 pagan GGGGG4
                                GGGBG3 mania GGGGG4
                                GGGGG3
                   BBBYG2 dandy BGGBG3 mangy GGGGG4
                                BGGGG3 handy GGGGG4
                                GGGGG3
                   BBGBB2 karma GGGGG3
                                YGGBG3 parka GGGGG4
                   BBGBG2 aphid YBBBB3 marry GGGGG4
                                YBYBB3 harry GGGGG4
                                YBYBY3 hardy GGGGG4
                                YYBBB3 parry GGGGG4
                                YYYBB3 harpy GGGGG4
                   BBYBB2 rabid GGBBB3 rajah GGGGG4
                                GGBBY3 radar GGGGG4
                                GGBGG3 rapid GGGGG4
                                GGBGY3 radii GGGGG4
                                GGGGG3
                                GGGYB3 rabbi GGGGG4
                   BBYBG2 ahead YBBBB3 fairy GGGGG4
                                YBBBY3 dairy GGGGG4
                                YYBBB3 hairy GGGGG4
                   BBYGG2 rainy GGGGG3
                   BBYYB2 nadir GGGGG3
                   BBYYG2 randy GGGGG3
                   BYBBB2 mambo GGGGG3
                   BYBBY2 bayou GGGGG3
                   BYBYB2 banjo BGGBG3 mango GGGGG4
                                BGYBY3 wagon GGGGG4
                                GGGGG3
                   BYGYB2 baron GGGGG3
                   BYYBB2 mover BYBBG3 razor GGGGG4
                                BYBBY3 radio GGGGG4
                                BYGBG3 favor GGGGG4
                                BYYBG3 vapor GGGGG4
                                GYBBG3 major GGGGG4
                   BYYBY2 mayor GGGGG3
                   BYYYB2 manor GGGGG3
                   BYYYY2 rayon GGGGG3
                   GBBBG2 cabby GGBBG3 caddy GGGGG4
                                GGGGG3
                   GBBGG2 canny GGGGG3
                   GBBYB2 cabin GGGGG3
                   GBBYG2 candy GGGGG3
                   GBGBG2 carry GGGGG3
                   GBYYB2 cairn GGGGG3
                   GYBBB2 cacao GGGGG3
                   GYBYB2 canon GGGGG3
                   GYGBB2 cargo GGGGG3
                   YBBBB2 macaw GGGGG3
                                GGYBB3 magic GGGGG4
                   YBBBG2 wacky GGGGG3
                   YBBYB2 manic BGGGG3 panic GGGGG4
                                GGGGG3
                   YBBYG2 fancy GGGGG3
                   YBGBB2 march GGGGG3
                   YBYYB2 ranch GGGGG3
                   YYBBB2 havoc GGGGG3
                                YGBYY3 macho GGGGG4
                   YYBYB2 bacon GGGGG3
                   YYYBB2 macro GGGGG3
      BGBBG1 thing GBBBB2 tarot GGGGG3
                   GBBGB2 taunt GGGGG3
                   GBGGB2 taint GGGGG3
                   GBYBB2 tacit GGGGG3
                   YBBBB2 caput GGBBG3 carat GGGGG4
                                GGGGG3
                   YBBBY2 gamut GGGGG3
                   YBBGB2 avoid YBBBB3 jaunt GGGGG4
                                YBBBY3 daunt GGGGG4
                                YYBBB3 vaunt GGGGG4
                   YBBGY2 gaunt GGGGG3
                   YBGGB2 faint BGGGG3 paint GGGGG4
                                GGGGG3
                   YYBBB2 yacht GGGGG3
                   YYBGB2 haunt GGGGG3
                   YYYBB2 habit GGGGG3
      BGBBY1 corby BBBBB2 datum BGYBB3 faith GGGGG4
                                GGGGG3
                   BBBBG2 faint BGBBY3 patty BGGGG4 tatty GGGGG5
                                             GGGGG4
                                BGBGY3 tawny GGGGG4
                                BGBYY3 tangy GGGGG4
                                GGBBY3 fatty GGGGG4
                                YGBBY3 taffy GGGGG4
                   BBBGG2 tabby GGGGG3
                   BBBYG2 batty GGGGG3
                   BBGBG2 party BGGGG3 warty GGGGG4
                                BGGYG3 tardy GGGGG4
                                GGGGG3
                   BBYBB2 tapir GGGGG3
                   BBYBG2 ratty GGGGG3
                   BYBBB2 patio BGYBG3 tango GGGGG4
                                GGGGG3
                   BYBYB2 baton GGGGG3
                                YGYGB3 taboo GGGGG4
                   BYYBB2 ratio GGGGG3
                   GBBBB2 cacti GGGGG3
                                GGYYB3 catch GGGGG4
                   GBBBG2 catty GGGGG3
                   YBBBB2 humph BBBBG3 watch GGGGG4
                                BBBYG3 patch GGGGG4
                                BBYBG3 match GGGGG4
                                GBBBG3 hatch GGGGG4
                   YBBBG2 tacky GGGGG3
                   YBBYB2 batch GGGGG3
      BGBGB1 gormy BBBBB2 haven BGBGG3 waxen GGGGG4
                                GGGGG3
                   BBBBY2 payee GGGGG3
                   BBGBB2 parer BGGGG3 rarer GGGGG4
                                GGGGG3
                   BBGYB2 harem GGGGG3
                   BBYBB2 caper BGBGG3 wafer BGBGG4 baker GGGGG5
                                             GGBGG4 waver GGGGG5
                                             GGGGG4
                                BGBGY3 raven GGGGG4
                                BGGGG3 paper GGGGG4
                                GGGGG3
                                YGBGG3 racer GGGGG4
                   BBYBY2 payer GGGGG3
                   BBYYB2 maker GGGGG3
                                YGBGY3 ramen GGGGG4
                   BYBBB2 oaken GGGGG3
                   BYBYB2 cameo GGGGG3
                   GBYBB2 gazer GGGGG3
                   GBYBY2 gayer GGGGG3
                   GBYYB2 gamer GGGGG3
                   YBBBG2 cagey GGGGG3
                   YBYBB2 eager BGGGG3 wager GGGGG4
                                GGGGG3
      BGBGG1 cadet GGGGG2
                   YGBGG2 facet GGGGG3
      BGBGY1 meter BBGGG2 awash YBBBB3 cater GGGGG4
                                YBBBY3 hater GGGGG4
                                YYBBB3 water GGGGG4
                   BBYGB2 taken GGGGG3
                   BBYGG2 taker GGBGG3 taper GGGGG4
                                GGGGG3
                   BYGGB2 eaten GGGGG3
                   BYGGG2 eater GGGGG3
                   GBGGB2 matey GGGGG3
                   YBYGG2 tamer GGGGG3
      BGBYB1 crumb BBBBB2 naive BGBBG3 gaffe GGGGG4
                                BGGGG3 waive GGGGG4
                                GGGGG3
                   BBBBY2 badge GGGGG3
                   BBBYB2 maize GGBBG3 mange GGGGG4
                                GGGGG3
                   BBBYY2 maybe GGGGG3
                   BBGBB2 gauge GGGBG3 gauze GGGGG4
                                GGGGG3
                   BBGYB2 mauve GGGGG3
                   BBYBB2 vague GGGGG3
                   BYBBB2 range GGGGG3
                   BYBBY2 barge GGGGG3
                   GBBBB2 cache GGBBG3 canoe GGGGG4
                                GGGGG3
                   GYBBB2 carve GGGGG3
                   YBBBB2 dance GGGGG3
                   YYBBB2 farce GGGGG3
      BGBYY1 bathe BGYYG2 haute GGGGG3
                   BGYYY2 earth GGGGG3
                   GGGGG2
      BGGBB1 rally BGGBB2 valid GGGGG3
                   BGGBG2 balmy GGGGG3
                   BGGGG2 dally GGGGG3
                   GGGBB2 ralph GGGGG3
                   GGGGG2
                   YGGBB2 valor GGGGG3
      BGGBY1 tally GGGBB2 talon GGGGG3
                   GGGGG2
                   YGGBB2 waltz GGGGG3
      BGGGB1 baler BGGGG2 paler GGGGG3
                   GGGGG2
      BGGGG1 valet GGGGG2
      BGGYB1 halve BGGGG2 valve GGGGG3
                   BGGYG2 value GGGGG3
                   GGGGG2
      BGYBB1 bingy BBBBB2 carol BGBBG3 papal GGGGG4
                                BGGBY3 larva GGGGG4
                                GGBBY3 caulk GGGGG4
                                GGGGG3
                   BBBBG2 madly GGGGG3
                   BBBGB2 laugh GGGGG3
                   BBBYG2 gayly GGGGG3
                   BBGBB2 canal GGGGG3
                   BBGBG2 lanky GGGGG3
                                YGGBG3 manly GGGGG4
                   BBYBB2 naval GGGGG3
                   BYBBB2 cavil GGGGG3
                   BYBBG2 daily GGGGG3
                   BYBYG2 gaily GGGGG3
                   GBBBG2 badly GGGGG3
                   GBGBB2 banal GGGGG3
                   YBBBB2 cabal BGGBY3 labor GGGGG4
                                GGGGG3
      BGYBG1 fault BGGGG2 vault GGGGG3
                   GGGGG2
      BGYBY1 fatal BGGBY2 latch GGGGG3
                   BGGGG2 natal GGGGG3
                   GGGGG2
      BGYGB1 lingy GBBBB2 label GGBGG3 lapel GGGGG4
                                GGGGG3
                   GBBBY2 layer GGGGG3
                   GBBYB2 lager GGGGG3
                   GBYBB2 laden GGGGG3
                   YBBBB2 camel BGBGG3 hazel GGGGG4
                                GGGGG3
                   YBBYB2 bagel BGYGG3 gavel GGGGG4
                                GGGGG3
                   YBGBB2 panel GGGGG3
                   YBYBB2 navel GGGGG3
      BGYGY1 later GGGGG2
      BGYYB1 creme BBBBG2 fable BGBGG3 ladle GGGGG4
                                GGGGG3
                   BBBYG2 maple GGGGG3
                   BBYBG2 eagle GGGGG3
                   BYBBG2 large GGGGG3
                   BYYBB2 early GGGGG3
                   GBBBG2 cable GGGGG3
                   YBBBG2 lance GGGGG3
      BGYYY1 lathe GGGBG2 latte GGGGG3
                   GGGGG2
                   YGYBG2 table GGGGG3
      BYBBB1 brond BBBBB2 chaff BBGBB3 guava GGGGG4
                                BBYBB3 pizza GGGGG4
                                BBYYY3 affix GGGGG4
                                BGGBB3 khaki GGGGG4
                                GGGBB3 champ GGGGG4
                                GGGGG3
                                YBGBB3 quack GGGGG4
                                YGGBB3 whack GGGGG4
                   BBBBG2 aphid GGGGG3
                   BBBGB2 aging GBGGG3 aping GGGGG4
                                GGGGG3
                                YBGGB3 china GGGGG4
                   BBBYB2 again BBGBY3 knack GGGGG4
                                BBGGG3 chain GGGGG4
                                GBYYG3 avian GGGGG4
                                GGGGG3
                                YBBBG3 human GGGGG4
                                YBBYY3 ninja GGGGG4
                   BBBYY2 admin GGGGG3
                   BBGBG2 avoid GGGGG3
                   BBGGB2 agony GGGGG3
                                GYGGB3 among GGGGG4
                   BBYBB2 coach BGGBB3 foamy GGGGG4
                                BYYBB3 axiom GGGGG4
                                GGGGG3
                                GGYBB3 comma GGGGG4
                                GGYYB3 cocoa GGGGG4
                                YGYBY3 mocha GGGGG4
                   BBYBY2 audio GGGGG3
                                YBGBY3 vodka GGGGG4
                                YBYBY3 dogma GGGGG4
                   BBYGB2 piano GGGGG3
                   BBYYB2 annoy GGGGG3
                                GYBGB3 axion GGGGG4
                                YYBYB3 woman GGGGG4
                   BBYYG2 gonad BGYGG3 nomad GGGGG4
                                GGGGG3
                   BGBBB2 copay BBBGB3 friar GGGGG4
                                BBBGG3 array GGGGG4
                                BBBYG3 gravy GGGGG4
                                BBYYB3 graph GGGGG4
                                GBBYB3 crack GGGGG4
                                GBBYG3 crazy GGGGG4
                                GBYYB3 cramp GGGGG4
                                YBBYB3 wrack GGGGG4
                   BGBBG2 fraud GGGGG3
                   BGBBY2 drama GGGGG3
                   BGBGB2 bicep BBBBB3 frank GGGGG4
                                BBBBY3 prank GGGGG4
                                BBYBB3 crank GGGGG4
                   BGBGG2 grand GGGGG3
                   BGBGY2 drank GGGGG3
                   BGBYB2 grain BGGBG3 prawn GGGGG4
                                GGGGG3
                   BGBYY2 drain GGGBG3 drawn GGGGG4
                                GGGGG3
                   BGGBB2 aroma GGGGG3
                                YGGBB3 croak GGGGG4
                   BGGYB2 groan GGGGG3
                   BGYBB2 armor GGBGY3 arrow GGGGG4
                                GGGGG3
                   BGYBY2 ardor GGGGG3
                   BGYYB2 organ GGGGG3
                   BYBBB2 chair BBGBY3 quark GGGGG4
                                BBYBG3 augur GGGGG4
                                BGGBY3 wharf GGGGG4
                                GBYYG3 cigar GGGGG4
                                GBYYY3 circa GGGGG4
                                GGGBY3 charm GGGGG4
                                GGGGG3
                                YBYYG3 vicar GGGGG4
                   BYBBG2 acrid GBYBG3 award GGGGG4
                                GGGGG3
                                YBYBG3 guard GGGGG4
                                YYYBG3 chard GGGGG4
                   BYBBY2 diary GBGGB3 dwarf GGGGG4
                                GGGGG3
                   BYBYB2 angry GGGGG3
                   BYGBB2 agora GGGGG3
                   BYGYB2 acorn GGGGG3
                   BYGYY2 adorn GGGGG3
                   BYYBB2 foray BGYYB3 roach GGGGG4
                                BYYYG3 ovary GGGGG4
                                GGGGG3
                   BYYBG2 hoard GGGGG3
                   BYYYB2 apron GGGGG3
                   GGBBB2 briar GGGGG3
                   GGBBG2 braid GGGGG3
                   GGBGG2 brand GGGGG3
                   GGBYB2 brain GGGBG3 brawn GGGGG4
                                GGGGG3
                   GGGBG2 broad GGGGG3
                   GGYBB2 bravo GGGGG3
                   GYYBB2 borax GGGGG3
                   GYYBG2 board GGGGG3
                   YBBBB2 aback GGGGG3
                   YGBYB2 urban GGGGG3
                   YGYBB2 arbor GGGGG3
                   YYBBB2 rumba GGGGG3
                                YYYYG3 umbra GGGGG4
                   YYYBB2 abhor GGGGG3
                                YYBYY3 cobra GGGGG4
      BYBBG1 courd BBBBB2 await BBGYG3 giant GGGGG4
                                GGGGG3
                   BBBBY2 adapt GGBBG3 admit GGGGG4
                                GGGGG3
                   BBBGB2 apart GGGGG3
                   BBBYB2 graft BGGBG3 trait GGGGG4
                                GGGBG3 grant GGGGG4
                                GGGGG3
                   BBBYY2 draft GGGGG3
                   BBYBY2 audit GGGGG3
                   BBYGB2 quart GGGGG3
                   BYBBB2 abbot GBBGG3 afoot GGGGG4
                                GGGGG3
                   BYBBY2 adopt GGGGG3
                   BYBGB2 abort GGGGG3
                   BYYBB2 about GGGGG3
                   GBBBB2 chant GGGGG3
                   GBBGB2 chart GGGGG3
                   GBBYB2 craft GGGGG3
                   YBBYB2 tract GGGGG3
      BYBBY1 tonic GBBBB2 tramp GGGGG3
                   GBBBY2 track GGGGG3
                   GBBGB2 tibia GGGGG3
                   GBBYB2 tiara GGGGG3
                                GYYYB3 triad GGGGG4
                   GBYBB2 thank GBGGB3 twang GGGGG4
                                GGGGG3
                   GBYGB2 train GGGGG3
                   GBYYB2 titan GGGGG3
                   GGBBB2 today GGBGB3 topaz GGGGG4
                                GGGGG3
                   GGGBB2 tonga GGGGG3
                   YBBBB2 wrath GGGGG3
                   YBBGG2 attic GGGGG3
                   YBBYB2 amity GGGGG3
                   YBGBB2 aunty GGGGG3
                                YGGGB3 junta GGGGG4
                   YBYGG2 antic GGGGG3
                   YGBBB2 aorta GGGGG3
                   YYBBB2 quota GGGGG3
                   YYBBY2 actor GGGGG3
      BYBGB1 incur BBBBB2 abbey GGGGG3
                   BBBBG2 amber GGGGG3
                   BBBBY2 agree GGGGG3
                   BGBBB2 annex GGGGG3
                   BGBBG2 anger GGGGG3
                   BYBBB2 apnea GGGGG3
                   YBBBG2 aider GGGGG3
      BYBGY1 after GGGGG2
      BYBYB1 beard BGGBB2 heave BGGBG3 peace GGGGG4
                                BGGGG3 weave GGGGG4
                                GGGGB3 heavy GGGGG4
                                GGGGG3
                                YGGBB3 peach GGGGG4
                   BGGBY2 heady GGGGG3
                   BGGGB2 weary BGGGB3 rearm GGGGG4
                                BGGGY3 yearn GGGGG4
                                GGGGG3
                   BGGGG2 heard GGGGG3
                   BGGYB2 reach GGGGG3
                   BGGYY2 ready GGGGG3
                   BGYBB2 mecca BGBBY3 vegan GGGGG4
                                BGGBY3 pecan GGGGG4
                                GGGGG3
                   BGYBY2 decay GGGGG3
                                YGBYB3 media GGGGG4
                   BGYYB2 recap GGBGY3 repay GGGGG4
                                GGGGG3
                   BGYYY2 cedar GGGGG3
                   BYGBB2 aking GBBBB3 amaze GGGGG4
                                GBBBY3 agape GGGGG4
                                GYBBB3 awake GGGGG4
                                YBBBB3 chafe GGGGG4
                                YBYBY3 image GGGGG4
                                YBYGB3 inane GGGGG4
                                YYBBB3 quake GGGGG4
                                YYBYB3 knave GGGGG4
                   BYGBY2 adage BYGBG3 evade GGGGG4
                                GGGGG3
                   BYGGB2 aware GGGGG3
                   BYGYB2 cezve BBBBG3 frame BGGBG4 grape GGGGG5
                                             GGGGG4
                                BBBGG3 grave GGGGG4
                                BBYBG3 graze GGGGG4
                                GBBBG3 crane GGGGG4
                                GBBGG3 crave GGGGG4
                                GBYBG3 craze GGGGG4
                                YBBBG3 grace GGGGG4
                   BYGYY2 drake GGGBG3 drape GGGGG4
                                GGGGG3
                                YGGBG3 grade GGGGG4
                   BYYBB2 enema BBGBY3 cheap GGGGG4
                                BBGYG3 omega GGGGG4
                                BYGBG3 hyena GGGGG4
                                BYGBY3 ocean GGGGG4
                                GGGGG3
                                YBBBY3 awoke GGGGG4
                                YGBGY3 anime GGGGG4
                   BYYBG2 ahead BBGGG3 knead GGGGG4
                                GBGBG3 amend GGGGG4
                                GGGGG3
                   BYYBY2 anode GGGGG3
                   BYYGB2 afire GBBGG3 azure GGGGG4
                                GGGGG3
                                YBBGY3 opera GGGGG4
                   BYYGY2 adore GGGGG3
                   BYYYB2 fleck BBGBB3 arena GGGGG4
                                BBGBG3 wreak GGGGG4
                                BBGYB3 cream GGGGG4
                                BBGYG3 creak GGGGG4
                                BBYBB3 argue GGGGG4
                                GBGBG3 freak GGGGG4
                   BYYYG2 dread GGGGG3
                   BYYYY2 dream GGGGG3
                   GGGBB2 beach GGGGG3
                   GGGBY2 beady GGGGG3
                   GGGGG2
                   GGYBB2 began GGGGG3
                   GYGYB2 aback BYGBB3 brave GGGGG4
                                BYGBY3 brake GGGGG4
                                BYGGB3 brace GGGGG4
                   GYYYB2 break GGGGG3
                   GYYYG2 bread GGGGG3
                   YGYBB2 kebab GGGGG3
                   YGYGB2 zebra GGGGG3
                   YGYYB2 rebar GGGGG3
                                GGYGB3 rehab GGGGG4
                   YGYYY2 debar GGGGG3
                   YYYBB2 above GGGGG3
                   YYYBY2 abide GGBGG3 abode GGGGG4
                                GGGGG3
                                GYBYG3 adobe GGGGG4
      BYBYG1 cedar BGBGB2 begat GGGGG3
                   BGBYB2 meant GGGGG3
                   BGBYY2 heart GGGGG3
                   BYBGB2 wheat GGGGG3
                   BYBGY2 great BGGGG3 treat GGGGG4
                                GGGGG3
                   BYBYB2 agent GGGGG3
                   BYBYY2 avert GGGGG3
                   BYYYB2 adept GGGGG3
                   GYBGB2 cheat GGGGG3
                   YGBYY2 react GGGGG3
                   YYBYB2 enact GBGGG3 exact GGGGG4
                                GGGGG3
      BYBYY1 grate BBGGG2 abate BBGGG3 ovate GGGGG4
                                GGGGG3
                   BBGGY2 death BGGGB3 meaty GGGGG4
                                BGGGG3 heath GGGGG4
                                GGGGG3
                   BBGYY2 teach GGGGG3
                   BBYGG2 acute GGGGG3
                   BBYGY2 theta GGGGG3
                   BBYYG2 atone GGGGG3
                   BBYYY2 tweak GGGGG3
                   BGGGG2 crate BGGGG3 irate GGGGG4
                                GGGGG3
                   BGGYG2 trace GGGBG3 trade GGGGG4
                                GGGGG3
                   BGYYY2 tread GGGGG3
                   BYGYY2 teary GGGGG3
                   BYYYY2 extra GGGGG3
                                YBYGG3 terra GGGGG4
                   GGGGG2
                   YBGGG2 agate GGGGG3
      BYGBB1 allay BBGGB2 molar BGGGG3 polar GGGGG4
                                GGGGG3
                   BBGGG2 inlay GGGGG3
                   BBGGY2 bylaw GGGGG3
                   BYGGB2 lilac GGGGG3
                   GBGBB2 aglow GGGGG3
                   GGGBB2 allow GGGGG3
                   GGGBG2 alloy GGGGG3
                   GGGGG2
                   YBGBB2 polka GGGGG3
                   YYGBB2 villa GGGGG3
      BYGBG1 allot GGGGG2
      BYGGB1 abled GBGGB2 alley GGGGG3
                   GGGGG2
      BYGYB1 delay BGGGB2 relax GGGGG3
                   BGGGG2 relay GGGGG3
                   BGGYB2 fella GGGGG3
                   GGGGG2
      BYGYG1 eclat GGGGG2
      BYGYY1 delta GGGGG2
      BYYBB1 corni BBBBB2 amply GBBYB3 awful GGGGG4
                                GBGGG3 apply GGGGG4
                                GBGYB3 alpha GGGGG4
                                GGGGG3
                                GYBYB3 album GGGGG4
                                YBBYG3 flaky GGGGG4
                                YBGYB3 pupal GGGGG4
                                YBYYB3 plaza GGGGG4
                                YYBGB3 qualm GGGGG4
                                YYBYB3 llama GGGGG4
                   BBBBG2 alibi GGGGG3
                   BBBBY2 allay GYBGB3 axial GGGGG4
                                GYBYB3 avail GGGGG4
                                YGBBB3 plaid GGGGG4
                                YGYBB3 flail GGGGG4
                                YYBBB3 quail GGGGG4
                   BBBGB2 bifid BBBBB3 plank GGGGG4
                                BBBBG3 gland GGGGG4
                                BBYBB3 flank GGGGG4
                                GBBBB3 blank GGGGG4
                                GBBBG3 bland GGGGG4
                   BBBYB2 annul GGGGG3
                   BBBYY2 align GGGGG3
                                GYYBY3 anvil GGGGG4
                                YGYBG3 plain GGGGG4
                                YYYBY3 final GGGGG4
                   BBGBB2 mural BGGGG3 rural GGGGG4
                                GGGGG3
                   BBGBY2 viral GGGGG3
                   BBYBB2 brawl BGGGG3 drawl GGGGG4
                                BYGBY3 alarm GGGGG4
                                GGGGG3
                   BBYBY2 flair BYGGY3 grail GGGGG4
                                BYYYY3 rival GGGGG4
                                GGGGG3
                                GYGGY3 frail GGGGG4
                   BBYYB2 lunar GGGGG3
                   BGBBB2 loamy GGGGG3
                                GGYBY3 loyal GGGGG4
                                YGGBB3 koala GGGGG4
                                YGYYB3 modal GGGGG4
                   BGBBY2 voila GGGGG3
                   BGBYB2 zonal GGGGG3
                   BGGBB2 moral GGGGG3
                   BGYBB2 royal GGGGG3
                   BYBBB2 afoul GBGGY3 aloud GGGGG4
                                GGGGG3
                                GYGBY3 aloof GGGGG4
                                YGYBG3 offal GGGGG4
                   BYBBY2 viola GGGGG3
                   BYBGB2 along GGGGG3
                   BYYBB2 flora GGGGG3
                   GBBBB2 chalk GBGYB3 clamp GGGGG4
                                GBGYG3 clack GGGGG4
                                GGGGG3
                   GBBBY2 claim GGGGG3
                   GBBGB2 clang GGGGB3 clank GGGGG4
                                GGGGG3
                   GBYBB2 crawl GGGGG3
                   GGGBB2 coral GGGGG3
                   GYBBB2 cloak GGGGG3
                   YBBBB2 black BGGGG3 flack GGGGG4
                                GGGGG3
                   YBBBY2 iliac GGGGG3
                   YGBBB2 favor BYBYB3 local GGGGG4
                                BYYYB3 vocal GGGGG4
                                GYBYB3 focal GGGGG4
      BYYBG1 fling BGBBB2 bloat GGGGG3
                   BGBBY2 gloat GGGGG3
                   BGBGB2 plant GGGGG3
                   BGYBB2 plait GGGGG3
                   BYBBB2 adult GGGGG3
                   GGBBB2 float GGGGG3
                   YGBBB2 aloft GGGGG3
      BYYBY1 douar BBBGB2 vital GGGGG3
                   BBBGG2 altar GGGGG3
                   BBBGY2 trial GGGGG3
                   BBBYB2 aptly GGGGG3
                   BBBYY2 trail GGGBG3 trawl GGGGG4
                                GGGGG3
                   BBYGB2 tubal GGGGG3
                   BBYYY2 ultra GGGGG3
                   BGBGB2 tonal GGBGG3 total GGGGG4
                                GGGGG3
                   BGBYB2 loath GGGGG3
                   BYBGB2 octal GGGGG3
                   BYBYB2 atoll GGGGG3
                   YBBGB2 tidal GGGGG3
      BYYGB1 alien GGGGG2
                   GYBGY2 angel GGGGG3
      BYYGY1 alter GGGGG2
      BYYYB1 gnarl BBGBG2 email GGGGG3
                   BBGBY2 fehme BBBBG3 blade BGGBG4 place GGGGG5
                                             GGGBG4 blaze GGGGG5
                                             GGGGG4
                                BBBGG3 blame GGGGG4
                                BBYBG3 whale GGGGG4
                                BGBBB3 leaky GGGGG4
                                BGBBG3 leave GGGGG4
                                BGBYB3 mealy GGGGG4
                                BGYBB3 leach GGGGG4
                                GBBBG3 flake GGGGG4
                                GBBGG3 flame GGGGG4
                                YGBBB3 leafy GGGGG4
                   BBGGG2 pearl GGGGG3
                   BBGGY2 blare BGGGG3 flare GGGGG4
                                GGGGG3
                   BBGYY2 realm GGGGG3
                   BBYBG2 medal BGBGG3 fecal GGGGG4
                                BGGGG3 pedal GGGGG4
                                BGYGG3 decal GGGGG4
                                BYBGG3 equal GGGGG4
                                BYYGG3 ideal GGGGG4
                                GGGGG3
                   BBYBY2 spike BBBBG3 amble GGGGG4
                                BBBYY3 bleak GGGGG4
                                BBGBG3 alive GGGGG4
                                BBGGG3 alike GGGGG4
                                BGBBG3 apple GGGGG4
                                BYBBG3 ample GGGGG4
                                BYBBY3 plead GGGGG4
                   BBYYG2 feral GGGGG3
                   BBYYY2 clear GGGGG3
                   BGYBY2 ankle GGGGG3
                   BYGBY2 plane GGGGG3
                   BYGGY2 learn GGGGG3
                   BYYBG2 penal GGGGG3
                   BYYBY2 alone GGGGG3
                                YGBYY3 clean GGGGG4
                   BYYYG2 renal GGGGG3
                   GBGBY2 glade GGGBG3 glaze GGGGG4
                                GGGGG3
                   GBGGY2 glare GGGGG3
                   GBYBY2 gleam GGGGG3
                   GYYBY2 glean GGGGG3
                   YBYBG2 legal GGGGG3
                   YBYBY2 agile GGGGG3
                                GYBYG3 algae GGGGG4
                   YBYYG2 regal GGGGG3
                   YGYBY2 angle GGGGG3
      BYYYG1 pecan BGBYB2 dealt GGGGG3
                   BGBYY2 leant GGGGG3
                   BYBGB2 bleat GGGGG3
                   BYBYB2 alert GGGGG3
                                YYYBG3 exalt GGGGG4
                   BYYGB2 cleat GGGGG3
                   GYBGB2 pleat GGGGG3
                   YGBYB2 leapt GGGGG3
      BYYYY1 ample YBBYG2 elate GGGGG3
                   YBBYY2 fetal GGGGG3
                   YBYYG2 plate GGGGG3
                   YBYYY2 petal GGGGG3
                   YYBYY2 metal GGGGG3
      GBBBB1 unrip BBBBB2 shock GBGBY3 smoky GGGGG4
                                GBGGG3 smock GGGGG4
                                GBGYB3 scoff GGGGG4
                                GBYBB3 soggy GGGGG4
                                GGGBB3 showy GGGGG4
                                GGGBG3 shook GGGGG4
                                GGGGG3
                   BBBBG2 scoop GBGGG3 swoop GGGGG4
                                GGGGG3
                   BBBBY2 spoof GGGGB3 spook GGGGG4
                                GGGGG3
                   BBBYB2 sissy GGGGG3
                                GYBBB3 skiff GGGGG4
                                GYBGB3 swish GGGGG4
                   BBBYG2 skimp GGGGG3
                   BBBYY2 spicy GGGBG3 spiky GGGGG4
                                GGGGG3
                   BBGBB2 sorry GGGGG3
                   BBGGY2 sprig GGGGG3
                   BBYBB2 sword GGGGG3
                   BBYYB2 shirk GBGGG3 smirk GGGGG4
                                GGGGG3
                   BGBBB2 snowy GGGGG3
                   BGBBG2 snoop GGGGG3
                   BGBYB2 sniff GGGGG3
                   BYBBB2 shown GBGYG3 swoon GGGGG4
                                GBYBY3 synod GGGGG4
                                GGGGG3
                   BYBBY2 spoon GGGGG3
                   BYBGB2 sonic GGGGG3
                   BYBYB2 shiny GBGGB3 swing GGGGG4
                                GBGYB3 scion GGGGG4
                                GGGGG3
                   BYBYY2 spiny GGGGG3
                   BYYBB2 awash BBBYB3 scorn GGGGG4
                                BBBYY3 shorn GGGGG4
                                BGBYB3 sworn GGGGG4
                   YBBBB2 shuck GGGBB3 shush GGGGG4
                                GGGGG3
                   YBBGB2 squib GGGGG3
                   YBBYB2 sushi GGGGG3
                   YBGBB2 scrub GBGGB3 shrug GGGGG4
                                GBGGG3 shrub GGGGG4
                                GGGGB3 scrum GGGGG4
                                GGGGG3
                   YBGBG2 syrup GGGGG3
                   YBYBB2 scour GGGGG3
                   YGBBB2 snuck GGGBB3 snuff GGGGG4
                                GGGGG3
                   YYBBB2 agony BBBGB3 skunk GGGGG4
                                BBBGG3 sunny GGGGG4
                                BBYGB3 sound GGGGG4
                                BYBGB3 swung GGGGG4
                   YYBBY2 spunk GGGGG3
                   YYBYB2 suing GGGGG3
                   YYYBY2 spurn GGGGG3
      GBBBG1 churn BBBBB2 swift GGGGG3
                   BBBBY2 stint GGGGG3
                   BBBGB2 skirt GBBGG3 sport GGGGG4
                                GGGGG3
                   BBBGY2 snort GGGGG3
                   BBGBY2 stunt GGGGG3
                   BBGGB2 spurt GGGGG3
                   BBYBB2 spout GBGGG3 stout GGGGG4
                                GGGGG3
                   BBYBY2 snout GGGGG3
                   BBYYB2 strut GGGGG3
                   BGBBB2 shift GGBBG3 shoot GGGGG4
                                GGGGG3
                   BGBGB2 shirt GGBGG3 short GGGGG4
                                GGGGG3
                   BGGBY2 shunt GGGGG3
                   BGYBB2 shout GGGGG3
                   BYBBB2 sight GGGGG3
                   YBYBB2 scout GGGGG3
      GBBBY1 pinko BBBBB2 study GGGBB3 stuff GGGGG4
                                GGGGG3
                   BBBBY2 sooty GBGYB3 storm GGGGG4
                                GBGYG3 story GGGGG4
                                GGBGB3 south GGGGG4
                                GGGGB3 sooth GGGGG4
                                GGGGG3
                                GYGYB3 stood GGGGG4
                   BBBYB2 stuck GGGGG3
                   BBBYY2 stock GGGBG3 stork GGGGG4
                                GGGGG3
                   BBYBB2 stung GGGGG3
                   BBYBY2 stony GGGGG3
                   BBYYB2 stunk GGGGG3
                   BGBBB2 sixth GGGGB3 sixty GGGGG4
                                GGGGG3
                   BYBBB2 smith GBGYB3 stiff GGGGG4
                                GGGGG3
                   BYBBY2 stoic GGGGG3
                   BYBYB2 stick GGGGG3
                   BYYBB2 sting GGGGG3
                   BYYYB2 stink GGGGG3
                   YBBBB2 stump GGGGG3
                   YBBBY2 stomp GGGBG3 stoop GGGGG4
                                GGGGG3
                   YYBBB2 strip GGGGG3
      GBBGB1 hewer BBBGB2 spied GGGGG3
                   BBBGG2 apron BBGBB3 surer GGGGG4
                                BBYBB3 skier GGGGG4
                                BBYYB3 sober GGGGG4
                                BYYBB3 super GGGGG4
                   BBBGY2 siren GGGGG3
                   BBGGG2 sower GGGGG3
                   BBYGB2 sinew GGGGG3
                   BBYGY2 screw GGGGG3
                   BGBGB2 semen GGBGG3 seven GGGGG4
                                GGGGG3
                   BGBGG2 sever GGGGG3
                   BGGGG2 sewer GGGGG3
                   BYBGB2 speed GGGGG3
                   BYBGG2 sneer GGGGG3
                   BYBGY2 scree GBGGG3 spree GGGGG4
                                GGGGG3
                   BYYGB2 sweep GGGGG3
                   YBBGB2 shied GGGGG3
                   YBYGY2 shrew GGGGG3
                   YYBGB2 sheen GGGGB3 sheep GGGGG4
                                GGGGG3
                   YYBGG2 sheer GGGGG3
      GBBGG1 sheet GBGGG2 sweet GGGGG3
                   GGGGG2
      GBBGY1 acrid BBBBB2 steep GGGGG3
                   BBBBG2 steed GGGGG3
                   BBYBB2 steer GGGGG3
      GBBYB1 prink BBBBB2 seedy GGGGG3
                                GGYBB3 segue GGGGG4
                                GYBBB3 shove GGGGG4
                   BBBBY2 smoke GGGGG3
                   BBBGB2 scene GBBGG3 shone GGGGG4
                                GGBGG3 scone GGGGG4
                                GGGGG3
                   BBBYB2 sense GGGGG3
                   BBGBB2 seize GGGGG3
                   BBGGB2 shine GBGGG3 swine GGGGG4
                                GGGGG3
                   BBGYB2 snide GGGGG3
                   BBYBB2 siege GGGBG3 sieve GGGGG4
                                GGGGG3
                   BBYBG2 sheik GGGGG3
                   BBYYB2 since GGGBG3 singe GGGGG4
                                GGGGG3
                   BYBBB2 cough BBBBB3 serve GGGGG4
                                BBYBB3 serum GGGGG4
                                BBYGB3 surge GGGGG4
                                BYBBB3 swore GGGGG4
                                BYBBY3 shore GGGGG4
                                YYBBB3 score GGGGG4
                   BYBYB2 snore GGGGG3
                   BYGBB2 shire GGGGG3
                   BYYBB2 serif GGGGG3
                   YBBBB2 scope GGGGG3
                   YBBBG2 speck GGGGG3
                   YBBBY2 spoke GGGGG3
                   YBBGB2 spend GGGGG3
                   YBGBB2 spice GGGGG3
                   YBGBY2 spike GGGGG3
                   YBGGB2 spine GGGGG3
                   YBGYB2 snipe GGGGG3
                   YYBBB2 sperm GGGGG3
                                GGYGB3 spore GGGGG4
                   YYGBB2 spire GGGGG3
      GBBYG1 scent GBGBG2 swept GGGGG3
                   GBGGG2 spent GGGGG3
                   GGGGG2
      GBBYY1 minor BBBBB2 setup GGGGG3
                   BBBYB2 stoke GGGBG3 stove GGGGG4
                                GGGGG3
                   BBBYY2 store GGGGG3
                   BBYBY2 stern GGGGG3
                   BBYYB2 stone GGGGG3
                   BYBBB2 spite GBGGG3 suite GGGGG4
                                GGGGG3
                   BYYBB2 stein GGGGG3
                   YBBYB2 smote GGGGG3
                   YYBBB2 smite GGGGG3
      GBGBB1 silky GBGBG2 sully GGGGG3
                   GBGGG2 sulky GGGGG3
                   GGGBG2 silly GGGGG3
                   GGGGG2
                   GYGBB2 solid GGGGG3
      GBGBG1 split GGGGG2
      GBGYB1 solve GGGGG2
      GBYBB1 plink BGBBB2 slosh GGBBB3 slyly GGGGG4
                                GGBGG3 slush GGGGG4
                                GGGGG3
                   BGBGB2 slung GGGGG3
                   BGBGG2 slunk GGGGG3
                   BGGBB2 slimy GGGGG3
                   BGGBG2 slick GGGGG3
                   BGGGB2 sling GGGGG3
                   BGGGG2 slink GGGGG3
                   BYBBB2 shyly GBBGB3 scold GGGGG4
                                GBBGG3 surly GGGGG4
                                GBBYB3 scowl GGGGG4
                                GGGGG3
                   BYBBG2 skulk GGGGG3
                   BYBBY2 skull GGGGG3
                   BYGBB2 swill GGGBG3 swirl GGGGG4
                                GGGGG3
                   BYGBY2 skill GGGGG3
                   YGBBB2 slump GGBBG3 sloop GGGGG4
                                GGGBG3 slurp GGGGG4
                                GGGGG3
                   YYBBB2 spool GGGGG3
                   YYGBB2 spill GGGGG3
                   YYYBB2 spoil GGGGG3
      GBYBG1 spilt GBGGG2 stilt GGGGG3
                   GGGGG2
      GBYBY1 sloth GGGGG2
                   GYBYB2 still GGGGG3
                   GYGYB2 stool GGGGG3
      GBYGB1 sleek GGGGB2 sleep GGGGG3
                   GGGGG2
                   GYBGB2 spiel GGGGG3
      GBYGG1 sleet GGGGG2
      GBYGY1 steel GGGGG2
      GBYYB1 chime BBBBG2 slope GGGGG3
                   BBBBY2 spell GBGGG3 swell GGGGG4
                                GGGGG3
                   BBBYY2 smell GGGGG3
                   BBGBG2 slide GGGGG3
                   BBGGG2 slime GGGGG3
                   BBGYG2 smile GGGGG3
                   BGBBY2 shelf GGGGB3 shell GGGGG4
                                GGGGG3
                   YBGBG2 slice GGGGG3
      GBYYG1 slept GGGGG2
                   GYGBG2 smelt GGGGG3
                   GYGYG2 spelt GGGGG3
      GBYYY1 stole GGBGG2 style GGGGG3
                   GGGGG2
      GGBBB1 copsy BBBGG2 sassy GGGGG3
                   BBBYB2 sauna GGGGG3
                   BBBYG2 sandy GGBBG3 savvy GGGGG4
                                GGGGG3
                   BBGYG2 sappy GGGGG3
                   BYBYB2 savor GGGGG3
                   BYBYG2 savoy GGGGG3
                   YBBYG2 saucy GGGGG3
      GGBBG1 saint GGGGG2
      GGBBY1 satin GGGBB2 satyr GGGGG3
                   GGGGG2
      GGBGB1 safer GGBGG2 saner GGGGG3
                   GGGGG2
      GGBYB1 sauce GGGGG2
      GGBYY1 saute GGGGG2
      GGGBB1 avian YBBBB2 sally GGGGG3
                   YBBBG2 salon GGGGG3
                   YBBGB2 salad GGGGG3
                   YBBYB2 salsa GGGGG3
                   YYBBB2 salvo GGGGG3
      GGGBY1 salty GGGGG2
      GGGYB1 salve GGGGG2
      GGYBB1 sadly GGGGG2
      GYBBB1 cramp BBGBB2 shady GBGBG3 snaky GGGGG4
                                GGGBB3 shank GGGGG4
                                GGGBG3 shaky GGGGG4
                                GGGGG3
                                GYGBB3 swash GGGGG4
                   BBGBY2 spank GGGGG3
                                GGGYB3 spawn GGGGG4
                                GYGBB3 soapy GGGGG4
                   BBGGB2 swami GGGGG3
                   BBGGG2 swamp GGGGG3
                   BBGYB2 smash GGGGG3
                   BBGYY2 spasm GGGGG3
                   BBYBB2 squad GGGGG3
                   BBYGB2 sigma GGGGG3
                   BYGBB2 shard GGGGB3 shark GGGGG4
                                GGGGG3
                   BYGBG2 sharp GGGGG3
                   BYGBY2 spark GGGGG3
                   BYGYB2 swarm GGGGG3
                   BYYBB2 sonar GBBGG3 sugar GGGGG4
                                GGGGG3
                   BYYBY2 spray GGGGG3
                   YBGBB2 shack GBGGG3 snack GGGGG4
                                GGGGG3
                   YBGGG2 scamp GGGGG3
                   YBGYB2 smack GGGGG3
                   YBYBB2 scuba GGGGG3
                   YBYYB2 sumac GGGGG3
                   YYGBB2 scarf GGGGB3 scary GGGGG4
                                GGGGG3
                   YYYBG2 scrap GGGGG3
                   YYYYB2 scram GGGGG3
      GYBBG1 champ BBGBB2 start GGGGG3
                   BBGYB2 smart GGGGG3
                   BBYBB2 squat GGGGG3
                   BGGBB2 shaft GGGGG3
                   YBGBB2 scant GGGGG3
      GYBBY1 prink BBBBB2 staff GGGBB3 stash GGGGG4
                                GGGGG3
                                GYGBB3 swath GGGGG4
                   BBBBG2 stack GGGGG3
                   BBBGB2 stand GGGGG3
                   BBBGG2 stank GGGGG3
                   BBYBB2 staid GGGGG3
                   BBYYB2 stain GGGGG3
                   BYBBB2 straw GGGGB3 stray GGGGG4
                                GGGGG3
                   BYBBG2 stark GGGGG3
                   BYYBB2 stair GGGGG3
                   YBBBB2 stamp GGGGG3
                   YYBBB2 strap GGGGG3
      GYBYB1 pharm BBGBB2 snake GBGBG3 suave GGGGG4
                                GGGGG3
                   BBGGB2 scare GBGGG3 snare GGGGG4
                                GGGGG3
                   BBYBB2 sedan GGGGG3
                                GYBGY3 sneak GGGGG4
                   BBYYB2 swear GGGGG3
                   BBYYY2 smear GGGGG3
                   BGGBB2 avoid YBBBB3 shake GGGGG4
                                YBBBY3 shade GGGGG4
                                YYBBB3 shave GGGGG4
                   BGGBY2 shame GGGGG3
                   BGGGB2 share GGGGG3
                   BGYYB2 shear GGGGG3
                   YBGBB2 space GGGBG3 spade GGGGG4
                                GGGGG3
                   YBGGB2 spare GGGGG3
                   YBYBB2 sepia GGGGG3
                                GYYBY3 speak GGGGG4
                   YBYYB2 spear GGGGG3
                   YGGBB2 shape GGGGG3
      GYBYG1 sweat GGGGG2
      GYBYY1 grike BBBBG2 state GGGBG3 stave GGGGG4
                                GGGGG3
                   BBBBY2 stead GGGGB3 steam GGGGG4
                                GGGGG3
                   BBBGG2 stake GGGGG3
                   BBBYG2 skate GGGGG3
                   BBBYY2 steak GGGGG3
                   BYBBG2 stare GGGGG3
                   YBBBG2 stage GGGGG3
      GYGBB1 solar GGGGG2
      GYGBG1 splat GGGGG2
      GYYBB1 chill BBBBG2 snarl GGGGG3
                   BBBGG2 small GGGGG3
                   BBBYB2 slang GGGGG3
                   BBYBG2 snail GGGGG3
                   BBYYB2 slain GGGGG3
                   BGBBG2 shawl GGGGG3
                                GGYBG3 shoal GGGGG4
                   BGBGG2 shall GGGGG3
                   BYBYB2 slash GGGGG3
                   YBBGB2 adapt BBGBB3 scaly GGGGG4
                                BBGYB3 scalp GGGGG4
                                BYGBB3 scald GGGGG4
                   YBBYB2 slack GGGGG3
      GYYBG1 shalt GBGYG2 slant GGGGG3
                   GGGGG2
      GYYBY1 stalk GGGGB2 stall GGGGG3
                   GGGGG2
      GYYYB1 scale GBGGG2 shale GGGGG3
                   GBGYG2 slave GGGGG3
                   GGGGG2
      GYYYY1 slate GGGGG2
                   GYGYG2 stale GGGGG3
                   GYYYY2 steal GGGGG3
      YBBBB1 mucho BBBBB2 brisk BBBGB3 gypsy GGGGG4
                                BBYGB3 gipsy GGGGG4
                                BBYYB3 wispy GGGGG4
                                BGGGG3 frisk GGGGG4
                                BYYYY3 risky GGGGG4
                                GGGGG3
                   BBBBY2 dross BBGGB3 kiosk GGGGG4
                                BBYGB3 noisy GGGGG4
                                BBYGY3 bossy GGGGG4
                                BBYYB3 bison GGGGG4
                                BGGGG3 gross GGGGG4
                                BYYYB3 visor GGGGG4
                                GGGGG3
                   BBBGB2 fishy GGGGG3
                   BBBYB2 whisk GGGGG3
                   BBYBB2 crisp GGGGG3
                   BBYBG2 disco GGGGG3
                   BBYBY2 cross GGGGG3
                   BGBBB2 dusky BGGBG3 fussy GGGGG4
                                GGGGG3
                   BGBGB2 bushy BGGGG3 pushy GGGGG4
                                GGGGG3
                   BGBYB2 husky GGGBG3 hussy GGGGG4
                                GGGGG3
                   BYBBB2 using GGBBB3 usurp GGGGG4
                                GGGGG3
                                YYYBB3 virus GGGGG4
                   BYBBY2 bonus GGGGG3
                   BYBYB2 brush GGGGG3
                   BYGBB2 ficus GGGGG3
                   BYGBY2 focus GGGGG3
                   BYYYB2 crush GGGGG3
                   GBBBB2 missy GGGGG3
                   GBBBY2 mossy GGGGG3
                   GGBBB2 musky GGGGG3
                   GGBGB2 mushy GGGGG3
                   GGGBB2 mucus GGGGG3
                   GGYBB2 music GGGGG3
                   GYBBB2 minus GGGGG3
                   YBBBB2 prism GGGGG3
                   YBBBY2 bosom GGGGG3
                   YGBYB2 humus GGGGG3
      YBBBG1 moria BBBGB2 visit GGGGG3
                   BBBYB2 twist GGGGG3
                   BBGBB2 burst GGGGG3
                   BBGYB2 first GGGGG3
                   BBYBB2 crust BGBGG3 tryst GGGGG4
                                BGGGG3 trust GGGGG4
                                GGGGG3
                   BBYYB2 wrist GGGGG3
                   BGBBB2 boost BGBGG3 joust GGGGG4
                                GGGGG3
                   BGBGB2 posit GGGGG3
                   BGBYB2 chafe BBBBB3 joist GGGGG4
                                BBBYB3 foist GGGGG4
                                BYBBB3 hoist GGGGG4
                   BGGBB2 worst GGGGG3
                   BGYBB2 roost GGGGG3
                   BYBBB2 ghost GGGGG3
                   BYYBB2 frost GGGGG3
                   GBBYB2 midst GGGGG3
                   GGBYB2 moist GGGGG3
      YBBBY1 gourd BBBBB2 tipsy GGGGG3
                   BBGYB2 truss GGGGG3
                   BBYBB2 musty GGGGG3
                   BBYBY2 dusty GGGGG3
                   BBYYB2 rusty GGGGG3
                   BGBYB2 torso GGGGG3
                   BGYYB2 torus GGGGG3
                   GBYBB2 gusty GGGGG3
                   GYYBB2 gusto GGGGG3
      YBBGB1 rumor BBBBG2 wiser GGGGG3
                   BBBYB2 nosey GGGGG3
                   BBBYG2 poser GGGGG3
                   BBYBG2 miser GGGGG3
                   BGBBB2 bused GGGGG3
                   BYBBG2 usher GGGGG3
                   GBBBB2 risen GGGGG3
                   GBBBG2 riser GGGGG3
      YBBGG1 apron BBBBB2 beset GGGGG3
                   BBBBY2 unset GGGGG3
                   BBBYY2 onset GGGGG3
                   BBYBB2 reset GGGGG3
                   BGBBB2 upset GGGGG3
      YBBGY1 ester GGGGG2
      YBBYB1 rhone BBBBG2 geese BBBYG3 issue GGGGG4
                                GBBGG3 guise GGGGG4
                                GGGGG3
                   BBBBY2 guess BBYYB3 pesky GGGGG4
                                GGGGG3
                   BBBYG2 dense BYYYG3 ensue GGGGG4
                                GGGGG3
                   BBGBG2 goose BGGGG3 moose GGGGG4
                                GGGGG3
                   BBGYG2 noose GGGGG3
                   BBYBG2 poise BGBGG3 mouse GGGGG4
                                BYBGG3 obese GGGGG4
                                GGBGG3 posse GGGGG4
                                GGGGG3
                                YGBGG3 copse GGGGG4
                   BBYBY2 poesy GGGGG3
                   BBYYG2 noise GGGGG3
                   BGBBY2 chess GGGGG3
                   BGGBG2 chose BGGGG3 whose GGGGG4
                                GGGGG3
                   BYYBG2 house GGGGG3
                   GBBBG2 reuse GGGGG3
                   GBBBY2 rebus GGGGG3
                   GBBYG2 rinse GGGGG3
                   GBBYY2 resin GGGGG3
                   GBYBG2 rouse GGGGG3
                   YBBBG2 curse BBGGG3 verse GGGGG4
                                BGGGG3 purse GGGGG4
                                GGGGG3
                   YBBBY2 acrid BBYBB3 press GGGGG4
                                BBYBY3 dress GGGGG4
                                BYYBB3 cress GGGGG4
                   YBBYG2 nurse GGGGG3
                   YBGBG2 prose GGGGG3
                   YBYBG2 worse GGGGG3
                   YBYBY2 verso GGGGG3
                   YYBBY2 fresh GGGGG3
                   YYYBG2 horse GGGGG3
      YBBYG1 quich BBBBB2 wrest GGGGG3
                   BBBYB2 crest GGGGG3
                   BBBYY2 chest GGGGG3
                   BBGBB2 exist GGGGG3
                   BBGBY2 heist GGGGG3
                   BGBBB2 guest GGGGG3
                   GGBBB2 quest GGGGG3
      YBBYY1 troth BBBGB2 zesty GGGGG3
                   BBYGB2 pesto GGGGG3
                   GBBBB2 tense GGGGG3
                   GBBBY2 these GGGGG3
                   GBBGB2 testy GGGGG3
                   GBGBY2 those GGGGG3
                   GYBBB2 terse GGGGG3
                   YBBBB2 fetus GGGGG3
                   YBYBY2 ethos GGGGG3
      YBGGG1 islet GGGGG2
      YBGYB1 pulse BBGGY2 welsh GGGGG3
                   GGGGG2
      YBYBB1 boeuf BBBGB2 lupus GGGGG3
                   BBBYB2 plush GGGGG3
                   BBBYY2 flush GGGGG3
                   BGBGB2 locus GGGGG3
                   BGBYB2 lousy GGGGG3
                   BYBBB2 gloss GGGGG3
                   BYBBY2 floss GGGGG3
                   GBBBB2 bliss GGGGG3
                   GBBYB2 blush GGGGG3
      YBYBY1 lusty GGGGG2
      YBYGB1 loser GGGGG2
      YBYYB1 afoot BBBBB2 bless GGGGG3
                   BBGBB2 close GGGGG3
                   BBGYB2 loose GGGGG3
                   BBYBB2 louse GGGGG3
                   BYBBB2 flesh GGGGG3
      YGBBB1 crimp BBBBB2 gassy GGGGG3
                   BBBBY2 pansy GGGGG3
                   BBBYB2 mason GGGGG3
                   BBGBB2 daisy GGGGG3
                   BBYBB2 basin GGGGB3 basis GGGGG4
                                GGGGG3
                   BYBBB2 harsh GGGGG3
                   BYBBY2 raspy GGGGG3
                   BYBYB2 marsh GGGGG3
                   YBYBB2 basic GGGGG3
      YGBBG1 waist GGGGG2
      YGBBY1 nutty BBBGB2 pasta GGGGG3
                   BBBGG2 hasty BGGGG3 pasty GGGGG4
                                GGGGG3
                   BBGBG2 patsy GGGGG3
                   BBYGG2 tasty GGGGG3
                   GBBGG2 nasty GGGGG3
      YGBYB1 caper BGBYB2 masse GGGGG3
                   BGBYY2 raise GGGGG3
                   BGYYB2 pause GGGGG3
                   BGYYY2 parse GGGGG3
                   GGBYB2 cause GGGGG3
      YGBYY1 batch BGYBB2 patty BGBGB3 waste GGGGG4
                                BGYGB3 taste GGGGG4
                                GGBGB3 paste GGGGG4
                   BGYBY2 haste GGGGG3
                   BGYYB2 caste GGGGG3
                   GGYBB2 baste GGGGG3
      YGGBB1 palsy GGGGG2
      YGGYB1 false GGGGG2
      YGYBB1 basal BGGBY2 lasso GGGGG3
                   BGGGG2 nasal GGGGG3
                   GGGBG2 basil GGGGG3
                   GGGGG2
      YGYGB1 easel GGGGG2
      YGYYB1 lapse GGGGG2
      YYBBB1 crags BBGBG2 amass GGGGG3
                   BBGBY2 awash BBGGB3 quasi GGGGG4
                                BBGGG3 quash GGGGG4
                                GGGGG3
                   BBGYY2 gnash GGGGG3
                   BBYBG2 abyss GBBGG3 amiss GGGGG4
                                GGGGG3
                   BBYBY2 assay GGGGG3
                   BGGBG2 brass GGGGG3
                   BGGBY2 brash GGGGG3
                   BGGYG2 grass GGGGG3
                   BGGYY2 grasp GGGGG3
                   BGYBY2 arson GGGGG3
                   GBGBG2 chaos GGGGG3
                   GBGBY2 chasm GGGGG3
                   GGGBG2 crass GGGGG3
                   GGGBY2 crash GGGGG3
      YYBBG1 brace BBGBB2 toast GGGGG3
                   BBGYB2 coast GGGGG3
                   BBYBB2 angst GGGGG3
                   BBYYB2 ascot GGGGG3
                   BYGBB2 roast GGGGG3
                   GBGBB2 boast GGGGG3
      YYBBY1 artsy GGGGG2
                   YBYYB2 vista GGGGG3
                   YGYGB2 trash GGGGG3
      YYBGB1 ashen GGBGB2 askew GGGGG3
                   GGGGG2
      YYBGG1 asset GGGGG2
      YYBYB1 brash BBGGB2 cease GGGGG3
                   BBGGY2 chase BGGGG3 phase GGGGG4
                                GGGGG3
                   BBGYB2 usage GGGGG3
                   BBYGB2 amuse GGGGG3
                   BBYYB2 aside GGGGG3
                                YGBBY3 essay GGGGG4
                   BGGGB2 erase GGGGG3
                   BGYGB2 arise GGBGG3 arose GGGGG4
                                GGGGG3
                   YBGGB2 abase GGGGG3
                   YBYGB2 abuse GGGGG3
      YYBYG1 abbey YBBYB2 feast GGGGG3
                   YBBYY2 yeast GGGGG3
                   YYBYB2 beast GGGGG3
      YYBYY1 tease GGGGG2
      YYYBB1 chals BBGGY2 psalm GGGGG3
                   BBGYG2 glass GGGGG3
                   BBGYY2 flask GGGGG3
                   BBYYY2 usual GGGGG3
                   BYGYY2 flash GGGGG3
                   GBGYG2 class GGGGG3
                   GBGYY2 clasp GGGGG3
                   GYGYY2 clash GGGGG3
      YYYBG1 blast GGGGG2
      YYYYB1 aisle GGGGG2
                   YBYYG2 lease GGGGG3
                   YBYYY2 leash GGGGG3
      YYYYG1 least GGGGG2
""".strip()



if __name__ == "__main__":
    strategy_lines = strategy.splitlines()    
    first_word = strategy_lines[0].split(" ")[0]

    clue_memo = {}

    def get_clue(guess, answer, epsilon = None):
        real_clues = ''
        if (guess, answer) in clue_memo:
            real_clues = clue_memo[(guess, answer)]

        else:
            for (i, letter) in enumerate(guess):
                if letter == answer[i]:
                    real_clues += 'G'
                elif letter in answer:
                    real_clues += 'Y'
                else:
                    real_clues += 'B'
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

    score = 0
    epsilon = 23
    G = 4

    # 35 successed at 95th percentile (105 total) -- 4 guess
    # 23 succeeds at 50th percentile (46 total)
    # 6.5 succeeds at 5th percentile (13 total)


    for answer in answers:

        # guess the optimal first word
        game_state = [first_word]
        turn = 1
        current_word = first_word
        clue = get_clue(current_word, answer, epsilon=epsilon)
        game_state.append(clue + str(turn))

        for g in range(G - 2):

            # guess the optimal second word for this clue
            current_word = get_optimal_guess(game_state)
            game_state.append(current_word)
            turn += 1
            clue = get_clue(current_word, answer, epsilon=epsilon)
            game_state.append(clue + str(turn))

        # Rather than use the optimal guess, which might not be in the answer list,
        # we'll try to find a word that is consistent with the two clues.
        final_guess = compute_final_guess(game_state)

        if final_guess == answer:
            score += 1

    print(f"Score: {score / len(answers) * 100:.4f}%")


