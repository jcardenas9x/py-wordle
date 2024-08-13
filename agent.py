import algo

from time import perf_counter
from rich.console import Console
from rich.progress import track
from helper import BattleType, load_corpus

class VoteeBattler:
    """
    All the internals of the battler are dependent on the parameters
    passed to it. Tuple:
    (
        wordLength -> Int: 5,
        guessAttempts -> Int: 6,
        battleType -> Int Enum: SINGLESEED
    )
    We derive word bank by loading the corpus of wordLength chars
    """
    def __init__(self, params=(5,6,BattleType.SINGLESEED.value)):
        (wordLength, guessAttempts, battleType) = params
        self.wordLength = wordLength
        self.guessAttempts = guessAttempts
        self.battleType = battleType
        self.wordBank = load_corpus(wordLength)
        
    def checkMode(self):
        """
        As a refresher:
        SINGLESEED = 1,
        BESTOFHUNDO = 2,
        BESTOF10000 = 3
        """
        return self.battleType
    
    def printOpsStatistics(self, wins, losses, guesses, mode, time_elapsed):
        avg_guesses = guesses / mode
        win_rate = wins / mode

        print("====== Results ======")
        print("Won {0} out of 100 tries".format(str(wins)))
        print("Lost {0} out of 100 tries".format(str(losses)))
        print("Avg guesses: {0}".format(str(avg_guesses)))
        print("Win rate against randomizer: {0}".format(str(win_rate)))
        print(f"Time elapsed: {time_elapsed:.6f} s")
    
    def runSingleSeed(self):
        print("Agent doing a single round against randomizer.")

        algo.run_random_guesser(self.wordBank, self.wordLength, self.guessAttempts, True)
    
    def runBestOfHundo(self):
        tries = 0
        guesses = 0
        wins = 0
        losses = 0
        start = perf_counter()

        for i in track(range(100), description="Agent battling against randomizer..."):
            soln = algo.run_random_guesser(self.wordBank, self.wordLength, self.guessAttempts)
            if soln > 0:
                wins += 1
                guesses += soln
            else:
                losses += 1
                guesses += 6
            tries += 1

        end = perf_counter() - start

        self.printOpsStatistics(wins, losses, guesses, 100, end)

    def runBestOf10000(self):
        tries = 0
        guesses = 0
        wins = 0
        losses = 0
        start = perf_counter()

        for i in track(range(10000), description="Agent battling against randomizer..."):
            soln = algo.run_random_guesser(self.wordBank, self.wordLength, self.guessAttempts)
            if soln > 0:
                wins += 1
                guesses += soln
            else:
                losses += 1
                guesses += 6
            tries += 1

        end = perf_counter() - start

        self.printOpsStatistics(wins, losses, guesses, 10000, end)
