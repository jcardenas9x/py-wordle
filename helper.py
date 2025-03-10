from enum import Enum

import os

class Feedback(Enum):
    correct = 2
    present = 1
    absent = 0

class BattleType(Enum):
    SINGLESEED = 1
    BESTOFHUNDO = 2
    BESTOF10000 = 3
    ## Add extra modes here. Don't forget to add it to modeMap.

    @classmethod
    def stringifyMode(cls, mode):
        modeMap = {
            BattleType.SINGLESEED.value: "Single Word Mode",
            BattleType.BESTOFHUNDO.value: "Best of 100 Words Mode",
            BattleType.BESTOF10000.value: "Best of 10000 Words Mode"
        }
        return modeMap[mode]

def parse_slot_feedback(enum_member_name):
    value = Feedback[enum_member_name].value

    return value

def load_corpus(size):
    wordList = []
    if size == 5 or size == 6:
        filename = "{}/corpus/corpus{}.txt".format(os.getcwd(),size)
        corpus_file = open(filename)
        for word in corpus_file:
            wordList.append(corpus_file.readline().strip())
        
        corpus_file.close()
    
    # if size is not valid, word list is empty
    return wordList

"""
load_optimal_score
'correct' corresponds to 2
therefore, the optimal score is 2 * size
default is 5. but we can change this depending on our needs.
"""
def load_optimal_score(size=5):
    return Feedback["correct"].value * size
