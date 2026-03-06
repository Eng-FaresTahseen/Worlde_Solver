from utils import *


if __name__ == "__main__":

    possible = ANSWERS.copy()

    print("\n" + "=" * 50)
    print("Feedback: g = green   y = yellow   r = grey")
    print("=" * 50 + "\n")

    counter = 0
    while True:
        if (counter == 0):
            top5 = [("soare", 5.9783), ("raise", 5.9479), ("salet", 5.9270), ("tares", 5.9194), ("raile", 5.9098)]
        else:
            top5 = top5_guesses(possible)
        
        counter += 1

        best_word = top5[0][0]

        print(f"Remaining words : {len(possible)}")
        print("Top 5 guesses   :")
        for (i, (w, h)) in enumerate(top5):
            print(f"  {i+1}. {w.upper():<10} {h:.4f} bits")
        print(f"BEST={best_word}")

        guess    = input("Your guess  : ").strip().lower()
        feedback = input("Feedback    : ").strip().lower()

        pattern = pattern_str_to_code(feedback)

        if (pattern == (2, 2, 2, 2, 2)):
            print("\nSolved!")
            break

        possible = filter_answers(possible, guess, pattern)

        if (len(possible) == 0):
            print("NO more words \nERROR")
            break

        print()