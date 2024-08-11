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
        description="Create a basic agent that tries to guess a random word against a Wordle-like API"
    )

    interface.add_argument('-l', '--length', 
                           type=int,
                           help="Determines how long the word to guess should be. Default is 5 letters",
                           )

    interface.add_argument('-g', '--guess',
                           type=int,
                           help="Define the number of guesses the agent should be allowed to make. Default is 6"
                           )
    
    interface.add_argument('-m', '--mode',
                           choices=[str(BattleType.SINGLESEED.value), str(BattleType.BESTOFHUNDO.value)],
                           help=f"Select the game's mode, {BattleType.SINGLESEED.value} for guessing a single random word (seed chosen from 1 - 9999) or {BattleType.BESTOFHUNDO.value} to test against 100 random words (seed chosen from 1 - 9999)"
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
