import json
import math
from collections import defaultdict


with open("targets_5_letter.json") as f:
    ANSWERS = json.load(f)

with open("dictionary_5_letter.json") as f:
    ALL_WORDS = json.load(f)


def get_pattern(guess, answer):
    pattern      = [0, 0, 0, 0, 0]
    answer_chars = list(answer)
    guess_chars  = list(guess)

    # greens
    for (i) in range(5):
        if (guess_chars[i] == answer_chars[i]):
            pattern[i]      = 2
            answer_chars[i] = None
            guess_chars[i]  = None

    # yellows
    for (i) in range(5):
        if (guess_chars[i] is not None and guess_chars[i] in answer_chars):
            pattern[i] = 1
            index = answer_chars.index(guess_chars[i])
            answer_chars[index] = None

    return tuple(pattern)


def calculate_entropy(guess, possible):
    pattern_counts = defaultdict(int)

    for (answer) in possible:
        pattern = get_pattern(guess, answer)
        pattern_counts[pattern] += 1

    total   = len(possible)
    entropy = 0.0

    for (count) in pattern_counts.values():
        p        = count / total
        entropy  = entropy - p * math.log2(p)

    return entropy


def top5_guesses(possible):
    if (len(possible) == 1):
        return [(possible[0], 0.0)]

    possible_set = set(possible)
    scores       = []

    for (word) in ALL_WORDS:
        h           = calculate_entropy(word, possible)
        is_possible = word in possible_set
        scores.append((word, h, is_possible))

    scores.sort(key=lambda x: (x[1], x[2]), reverse=True)

    result = []
    for (word, h, _) in scores[:5]:
        result.append((word, h))

    return result


def filter_answers(possible, guess, pattern):
    new_possible = []
    for (answer) in possible:
        if (get_pattern(guess, answer) == pattern):
            new_possible.append(answer)
    return new_possible


def pattern_str_to_code(text):
    color_map = {'g': 2, 'y': 1, 'r': 0}
    result = []
    for (c) in text.strip():
        result.append(color_map[c])
    return tuple(result)