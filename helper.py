from enum import Enum

class Feedback(Enum):
    correct = 2
    present = 1
    absent = 0

def parse_slot_feedback(enum_member_name):
    value = Feedback[enum_member_name].value

    return value

def load_corpus(size):
    wordList = []
    if size == 5 or size == 6:
        filename = "corpus{}.txt".format(size)
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
