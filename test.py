import math
import json
import random
from collections import defaultdict

with open('dictionary_5_letter.json', 'r') as f:
    data = json.load(f)

with open('targets_5_letter.json', 'r') as f:
    target_data = json.load(f)

def reset_data(data):
    with open('dictionary_5_letter.json', 'r') as f:
        data = json.load(f)
    return data

def generate_random_word(data):
    return random.choice(data)

def get_feedback(word , actual_word):
    result = ""
    for i in range(len(word)):
        if (word[i] == actual_word[i]):
            result += 'G'
        elif (word[i] in actual_word):
            result += 'Y'
        else:
            result += 'B'
    return result

def calc_information(probability):
    return -math.log2(probability)

def calculate_entropy(word , data):
    entropy_val = 0
    data_size = len(data)
    probs = defaultdict(float)
    for w in data :
        probs[get_feedback(word , w)] += 1/data_size
        pass
    for key , value in probs.items():
        entropy_val += value*calc_information(value) 
        pass
    return entropy_val

def get_maximum_entropy_word(data):
    entropy_max = -1
    max_word = None
    for i in data :
        x = calculate_entropy(i , data)
        if (x > entropy_max):
            entropy_max = x
            max_word = i
    return [max_word , entropy_max]

def filter_data(guessed_word, pattern, current_data):
    return [
        word for word in current_data
        if get_feedback(guessed_word, word) == pattern
    ]

def console_solve(actual_word , data):
    no_tries = 0
    history = []
    while(True):
        current_word , _ = ["tares" , None] if no_tries == 0 else get_maximum_entropy_word(data)
        print(f"I choose the word '{current_word}'  , Let's try .")
        current_feedback = get_feedback(current_word ,actual_word)
        history.append((current_word, current_feedback))
        data = filter_data(current_word, current_feedback, data)
        no_tries += 1
        if (actual_word == current_word):
            print("Yes ! , I finally get it")
            break
    print(f"I solve it in {no_tries} times , The word is {current_word}")
    return [no_tries , current_word]

def console_solve_external(data):
        no_tries = 0
        history = []
        while(True):
            current_word , _ = ["tares" , None] if no_tries == 0 else get_maximum_entropy_word(data)
            print(f"I choose the word '{current_word}'  , Let's try .")
            current_feedback = input("Enter the current feedback : ")
            history.append((current_word, current_feedback))
            data = filter_data(current_word, current_feedback, data)
            no_tries += 1
            if (current_feedback == "GGGGG"):
                print("Yes ! , I finally get it")
                break
        print(f"I solve it in {no_tries} times , The word is {current_word}")
        
        if (input("You want to solve another one ? [Yes/No]") == "Yes"):
            with open('dictionary_5_letter.json', 'r') as f:
                data = json.load(f)
            console_solve_external(data)
        else :
            return

console_solve_external(data)