# The 6.00 Word Game - My Implementation

import random
VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1,
    'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,'o': 1, 'p': 3, 'q': 10, 'r': 1,
    's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}
WORDLIST_FILENAME = "words.txt"


def loadwords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordList: list of strings
    wordList = tuple(line.strip().lower() for line in inFile)
    print("  ", len(wordList), "words loaded.")
    return set(wordList)


def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def getWordScore(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
    total = 0
    N = len(word)
    for i in range(N):
        total += SCRABBLE_LETTER_VALUES[word[i]]
    total *= len(word)
    if N == n:
        total += 50
    return total


def displayHand(hand):
    """
    Displays the letters currently in the hand.

    For example:
    displayHand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=" ")  # print all on the same line
    print()  # print an empty line


def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand = {}
    numVowels = n // 3

    for i in range(numVowels):
        x = VOWELS[random.randrange(0, len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1

    for i in range(numVowels, n):
        x = CONSONANTS[random.randrange(0, len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1

    return hand


#
# Problem #2: Update a hand by removing letters
#
def updateHand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    new = hand.copy()
    for letter in word:
        if letter in hand:
            new[letter] -= 1
    return new


def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.
   
    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    new = hand.copy()
    if word not in wordList:
        return False
    for letter in word:
        if new[letter] <= 0:
            return False
            break
        new[letter] -= 1
    return True


def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    total = 0
    for i in hand.values():
        total += i
    return total


def playHand(hand, wordList, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      wordList: list of lowercase strings
      n: integer (HAND_SIZE; i.e., hand size required for additional points)
      
    """
    score = 0

    while calculateHandlen(hand) > 0:
        print('current hand is:', end=' ')
        displayHand(hand)
        # Display the hand
        user = input('Enter word, or a "." to indicate that you are finished: ')
        # Ask user for input
        if user == '.':
            print('The round has ended as you inputted "." ')
            print('your total score for this round '
                  'is', score)
            break
        if isValidWord(user, hand, wordList) == False:
            print('invalid word, bro\n')
        else:
            print('Points gained is', getWordScore(user, n), end='. ')
            score += getWordScore(user, n)
            print('current score is', score, end='. ')
            print('\n')
            hand = updateHand(hand, user)
    if calculateHandlen(hand) == 0:
        print('You have used all of the word, Congrats! Your total score is:', score)
    return score


def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, tell them their input was invalid.
 
    2) When done playing the hand, repeat from step 1    
    """

    # Initialize an empty hand
    played = False
    final_score = 0
    n = 0
    # Loop until the user exits the game
    while True:
        # Ask the user to input 'n', 'r', or 'e'
        user = input("Enter n to deal a new hand, r to replay the last hand, or e to end game: ")
        # If the user inputs 'n', deal a new hand and play it
        if user == 'n':
            hand = dealHand(HAND_SIZE)
            temp = playHand(hand, wordList, HAND_SIZE)
            played = True
            final_score += temp
            n += 1
        # If the user inputs 'r', check if there is a previous hand and play it
        elif user == 'r':
            if played:
                temp = playHand(hand, wordList, HAND_SIZE)
                final_score += temp
                n += 1
            else:
                print("You have not played a hand yet")
                continue
        # If the user inputs 'e', exit the game
        elif user == 'e':
            print('your final score from playing', n, 'game(s) is', final_score)
            break
        # If the user inputs anything else, print an invalid message
        else:
            print("Invalid command.")


if __name__ == '__main__':
    wordList = loadwords()
    playGame(wordList)
