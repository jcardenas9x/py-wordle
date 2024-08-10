### internal deps
import algo

from time import perf_counter
from helper import load_corpus

if __name__ == "__main__":
    print("====== Wordle Parameters ======")
    print("WORD LENGTH: 5 (Wordle default)")
    print("GUESS ATTEMPTS: 6 (Wordle default)")

    wordList = load_corpus(5)

    tries = 0
    guesses = 0
    wins = 0
    losses = 0
    start = perf_counter()

    print("Agent battling against randomizer. This may take a while")

    while tries < 100:
        soln = algo.run_random_guesser(wordList, 5, 6)
        if soln > 0:
            wins += 1
            guesses += soln
        else:
            losses += 1
            guesses += 6
        tries += 1

    avg_guesses = guesses / 100
    win_rate = wins / 100
    end = perf_counter() - start

    print("====== Results ======")
    print("Won {0} out of 100 tries".format(str(wins)))
    print("Lost {0} out of 100 tries".format(str(losses)))
    print("Avg guesses: {0}".format(str(avg_guesses)))
    print("Win rate against randomizer: {0}".format(str(win_rate)))
    print(f"Time elapsed: {end:.6f} s")
