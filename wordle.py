### internal deps
import agent
from helper import BattleType

if __name__ == "__main__":
    print("Initializing battler...")

    Battler = agent.VoteeBattler((5,6,BattleType.SINGLESEED.value))

    if Battler.checkMode() == BattleType.SINGLESEED.value:
        Battler.runSingleSeed()
    elif Battler.checkMode() == BattleType.BESTOFHUNDO.value:
        Battler.runBestOfHundo()
