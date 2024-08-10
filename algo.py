from random import randrange, choice

import requests
import helper

VOTEE_WORDLE_API = 'https://wordle.votee.dev:8000/'

"""
guess_random_word
Connects to Votee Wordle API /random endpoint, to guess a word against seed
    the length of word arg should be equal to size arg
    by default, size is 5.
In theory, size can be higher or lower. Wordle locks to 5.
"""
def guess_random_word(word, seed, size=5):
    res = requests.get(
        VOTEE_WORDLE_API+"/random", 
        {"guess": word, "seed": seed, "size": size}
    )
    if res.status_code == 200:
        return res.json()
    else:
        return {"error": res.text}
    
"""
did_we_win
Accepts feature set + optional size.
Calculate the total score of the guess, if it is equal to optimal score,
we win! It returns Boolean
Optimal score for a 5 letter word is 10.
"""
def did_we_win(guess_feature_set, size=5):
    score = 0
    for feedback_value in guess_feature_set.values():
        score += feedback_value[1]
    return score == helper.load_optimal_score(size)

"""
validate_guess
Accepts response from the API server
It will return a tuple containing:
    guess_word - the word that was guessed
    guess_feature_set -
        the result feedback from the server, as a tuple of SIZE elements
        each element is coded
        2 = correct, 1 = present, 0 = absent. 
"""
def validate_guess(json_response):
    guess_feature_set = {}
    guess_word = ''.join([guess["guess"] for guess in json_response])
    for guessed_letter in json_response:
        guess_feature_set[guessed_letter["slot"]] = (
            guessed_letter["guess"],
            helper.parse_slot_feedback(guessed_letter["result"])
        )
        
    return (guess_word, guess_feature_set)

"""
run_guesser
parameters = size of the word. set to wordle default of 5
max_guesses = maximum number of guesses we give the agent. set to wordle default of 6
Algorithm sourced from 
    https://medium.com/@devin.p.quinn/solving-wordle-using-monte-carlo-tree-search-reinforcement-725562779c8b
"""
def run_random_guesser(size=5, max_guesses=6):    
    ## https://mitsloan.mit.edu/ideas-made-to-matter/how-algorithm-solves-wordle
    ## https://x.com/jshkatz/status/1560007611038289921
    word_guess = "salet"

    if size == 6:
        word_guess = "slates"

    alphabet = [chr(letter) for letter in range(ord('a'), ord('z') + 1)]
    corpus = helper.load_corpus(size)
    guesses = 0
    seed = randrange(1, 9999)

    """
    correct_letters is represented as a dict of SLOT_NUM:LETTER. 
    present and absent letters are list we use to compare to the corpus and trim/weight as needed
    """
    correct_letters = {}
    present_letters = []

    ## don't initialize this after each guess.
    yellowWeights = {}

    for guesses in range(1,max_guesses):
        greenWeights = {}
        currentGreenPool = []
        currentYellowPool = []

        (word, feature_set) = validate_guess(guess_random_word(word_guess, seed, size))

        if did_we_win(feature_set, size):
            print("Random word solved! The word was {0}".format(word))
            print("You needed {0} guess(es)".format(str(guesses)))
            return guesses
        
        for slot in feature_set:
            if feature_set[slot][1] == helper.Feedback.correct.value:
                correct_letters.update({slot: feature_set[slot][0]})
            elif feature_set[slot][1] == helper.Feedback.present.value:
                present_letters.append(feature_set[slot][0])
            elif feature_set[slot][1] == helper.Feedback.absent.value:
                if feature_set[slot][0] in alphabet:
                    alphabet.remove(feature_set[slot][0])

        ## Remove words from the corpus that contain absent letters.
        for word in reversed(corpus):
            for letter in word:
                if letter not in alphabet:
                    corpus.remove(word)
                    break
        
        ## Remove words from the corpus that do not contain letters in correct slots.
        for word in corpus:
            for slot, letter in list(correct_letters.items()):
                if word[slot] != letter:
                    corpus.remove(word)
                    break
        
        ## Start weighting the remaining words.
        ## Increase weight by 1 for every appearance of correct/present letter.
        for word in corpus:
            weight = 0
            for slot, letter in list(correct_letters.items()):
                if word[slot] == letter:
                    weight += 1
            greenWeights.update({word: weight})

        for word in corpus:
            weight = 0
            for letter in word:
                if letter in present_letters:
                    weight += 1
            yellowWeights.update({word: weight})

        ## Sort the green and yellow weighted lists...
        ## We want the words with the highest weight at the lowest index of the dictionary.
        ## Remember, we want Reverse = True since it's ASC sorted by default.
        greenWeights = {key: value for key, value in sorted(greenWeights.items(), key = lambda item: item[1], reverse=True)}
        yellowWeights = {key: value for key, value in sorted(yellowWeights.items(), key = lambda item: item[1], reverse=True)}

        ## Now we start constructing the candidate pools for the agent to guess.
        ## We have to exhaustively check the lists by matching weight to the highest weighted word.
        for word, weight in greenWeights.items():
            if weight == list(greenWeights.values())[0]:
                currentGreenPool.append(word)

        for word, weight in yellowWeights.items():
            if weight == list(yellowWeights.values())[0]:
                currentYellowPool.append(word)

        ## Generate base seed
        tree_seed = randrange(1, 10)

        ## Based on the seed, the guesser will choose between yellow words or green words.
        ## A much higher weight is emphasized on green words.
        ## Agent will randomly choose between candidate words with highest weights, ie. pool
        if tree_seed < 1:
            if len(currentYellowPool) > 0:
                word_guess = choice(currentYellowPool)
        else:
            if len(currentGreenPool) > 0:
                word_guess = choice(currentGreenPool)

    print(f"Failed to guess the random word after {max_guesses} attempts")
    return -1
