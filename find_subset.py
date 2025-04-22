import re

# grab all words with a GGGGG2

#      BBYGG1 fleet GGGGG2
#

pattern = "      [A-Za-z0-9]{6} ([a-z]{5}) GGGGG2"

# "                   BGBGY2 dowry GGGGG3"
pattern2 = "                   [A-Za-z0-9]{6} ([a-z]{5}) GGGGG3"

words = []
for line in open("strategy_normal.txt"):
    if re.match(pattern, line):
        words.append(re.match(pattern, line).group(1))
    elif re.match(pattern2, line):
        words.append(re.match(pattern2, line).group(1))



print(len(set(words))) # 924

with open("easy_words.txt", "w") as f:
    for word in set(words):
        f.write(word + "\n")
