# Problem Set 2, hangman.py
# Name:
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, guessed_letters):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    guessed_letters: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in guessed_letters;
      False otherwise
    '''
    for char in secret_word:
        if char not in guessed_letters:
            return False

    return True


def get_guessed_word(secret_word, guessed_letters):
    '''
    secret_word: string, the word the user is guessing
    guessed_letters: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word = ''
    for char in secret_word:
        if char not in guessed_letters:
            word += '_ '
        else:
            word += char

    return word


def get_available_letters(guessed_letters):
    '''
    guessed_letters: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = ''
    for char in string.ascii_lowercase:
        if char not in guessed_letters:
            available_letters += char

    return available_letters


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''

    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long')

    guesses_left = 6
    warnings_left = 3
    guessed_letters = []

    print(f'You have {warnings_left} warnings left')
    print('-------------')

    while True:
        print(f'You have {guesses_left} guesses left')
        print(f'Available letters: {get_available_letters(guessed_letters)}')

        new_letter = input('Please enter a letter: ').lower()
        guessed_word = get_guessed_word(secret_word, guessed_letters)

        if new_letter.isalpha():
            if new_letter not in guessed_letters:
                guessed_letters.append(new_letter)
                guessed_word = get_guessed_word(secret_word, guessed_letters)

                if new_letter in secret_word:
                    print(f'Good guess: {guessed_word}')
                else:
                    if new_letter in 'aeiou':
                        guesses_left -= 2
                    else:
                        guesses_left -= 1
                    print(
                        f'Oops! That letter is not in my word: {guessed_word}')
            else:
                if warnings_left > 0:
                    warnings_left -= 1
                    print(
                        f'Oops! You\'ve already guessed that letter. You now have {warnings_left} warnings: {guessed_word}')
                else:
                    guesses_left -= 1
                    print(
                        f'Oops! You\'ve already guessed that letter. You now have no warnings left so you lose one guess: {guessed_word}')

        else:
            if warnings_left > 0:
                warnings_left -= 1
                print(
                    f'Oops! That is not a valid letter. You have {warnings_left} warnings left: {guessed_word}')
            else:
                guesses_left -= 1
                print(
                    f'Oops! You\'ve already guessed that letter. You now have no warnings left so you lose one guess: {guessed_word}')

        print('-------------')

        if is_word_guessed(secret_word, guessed_letters):
            unique_letters = []
            for char in secret_word:
                if char not in unique_letters:
                    unique_letters.append(char)

            print('Congratulations, you won!')
            print(
                f'Your total score for this game is {guesses_left * len(unique_letters)}')
            break

        if guesses_left <= 0:
            print(f'Sorry, you ran out of guesses. The word was {secret_word}')
            break

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''

    no_spaces_word = ''
    guessed_letters = []
    for char in my_word:
        if char != ' ':
            no_spaces_word += char

        if char.isalpha():
            guessed_letters.append(char)

    if len(no_spaces_word.strip()) != len(other_word.strip()):
        return False

    for i in range(len(no_spaces_word)):
        current_letter = no_spaces_word[i]
        other_letter = other_word[i]
        if current_letter.isalpha():
            has_same_letter = current_letter == other_letter
            if not has_same_letter:
                return False
        else:
            if current_letter == '_' and other_letter in guessed_letters:
                return False

    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            matches.append(word)

    if len(matches) > 0:
        for word in matches:
            print(word, end=' ')
        print()
    else:
        print('No matches found')


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 

    Follows the other limitations detailed in the problem write-up.
    '''
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is {} letters long'.format(len(secret_word)))

    guesses_left = 6
    warnings_left = 3
    guessed_letters = []

    print(f'You have {warnings_left} warnings left')
    print('-------------')

    while True:
        print(f'You have {guesses_left} guesses left')
        print(f'Available letters: {get_available_letters(guessed_letters)}')

        guessed_letter = input('Please enter a letter: ').lower()
        guessed_word = get_guessed_word(secret_word, guessed_letters)

        if guessed_letter.isalpha():
            if guessed_letter not in guessed_letters:
                guessed_letters.append(guessed_letter)
                guessed_word = get_guessed_word(secret_word, guessed_letters)

                if guessed_letter in secret_word:
                    print(f'Good guess: {guessed_word}')
                else:
                    if guessed_letter in 'aeiou':
                        guesses_left -= 2
                    else:
                        guesses_left -= 1
                    print(
                        f'Oops! That letter is not in my word: {guessed_word}')
            else:
                if warnings_left > 0:
                    warnings_left -= 1
                    print(
                        f'Oops! You\'ve already guessed that letter. You now have {warnings_left} warnings: {guessed_word}')
                else:
                    guesses_left -= 1
                    print(
                        f'Oops! You\'ve already guessed that letter. You now have no warnings left so you lose one guess: {guessed_word}')
        elif guessed_letter == '*':
            print('Possible word matches are: ')
            show_possible_matches(guessed_word)
        else:
            if warnings_left > 0:
                warnings_left -= 1
                print(
                    f'Oops! That is not a valid letter. You have {warnings_left} warnings left: {guessed_word}')
            else:
                guesses_left -= 1
                print(
                    f'Oops! You\'ve already guessed that letter. You now have no warnings left so you lose one guess: {guessed_word}')

        print('-------------')

        if is_word_guessed(secret_word, guessed_letters):
            unique_letters = []
            for char in secret_word:
                if char not in unique_letters:
                    unique_letters.append(char)

            print('Congratulations, you won!')
            print(
                f'Your total score for this game is {guesses_left * len(unique_letters)}')
            break

        if guesses_left <= 0:
            print(f'Sorry, you ran out of guesses. The word was {secret_word}')
            break


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.
if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman_with_hints(secret_word)
