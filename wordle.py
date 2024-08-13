### external deps
import argparse

### internal deps
import agent
from helper import BattleType

if __name__ == "__main__":
    """
    Ingest cli parameters
    """ 

    interface = argparse.ArgumentParser(
        description="Create a basic agent that tries to guess a random word against a Wordle-like API",
        formatter_class=argparse.RawTextHelpFormatter
    )

    interface.add_argument('-l', '--length', 
                           type=int,
                           help="Determines how long the word to guess should be. Default is 5 letters",
                           default=5
                           )

    interface.add_argument('-g', '--guess',
                           type=int,
                           help="Define the number of guesses the agent should be allowed to make. Default is 6",
                           default=6
                           )
    
    interface.add_argument('-m', '--mode',
                           choices=[str(BattleType.SINGLESEED.value), str(BattleType.BESTOFHUNDO.value), str(BattleType.BESTOF10000.value)],
                           help='''With random seed 1 to 9999, picks the game mode:
    1 - Agent guesses against a single word
    2 - Agent guesses against 100 words
    3 - Agent guesses against 10000 words
                            ''',
                           default=1
                           )

    args = interface.parse_args()
    gameMode = int(args.mode)

    print("==== Initializing Battler ====")
    print(f"Word Length: {args.length}")
    print(f"Guesses: {args.guess}")
    print(f"Game Mode: {BattleType.stringifyMode(gameMode)}")
    print("==============================")

    params = (args.length, args.guess, gameMode)
    battler = agent.VoteeBattler(params)

    if gameMode == BattleType.SINGLESEED.value:
        battler.runSingleSeed()
    elif gameMode == BattleType.BESTOFHUNDO.value:
        battler.runBestOfHundo()
