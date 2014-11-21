__author__ = 'Wanchun Zhao'

from Player import Player
from string import maketrans
import random

#read wheel puzzles from a file, store them in a list, and return the list
def read_wheel_puzzles():
    wheel_puzzles_file = open("wheel_puzzles.txt")
    wheel_puzzles = list()

    for line in wheel_puzzles_file:
        wheel_puzzles.append(line.rstrip())

    wheel_puzzles_file.close()

    return wheel_puzzles


#read wheel values from a file, store them in a list, and return the list
def read_wheel_values():
    wheel_values_file = open("wheel_values.txt")

    wheel_values = list()
    for line in wheel_values_file:
        wheel_values.append(line.rstrip())

    wheel_values_file.close()

    return wheel_values


#randomly chosen wheel_value from the wheel_values list
def spin_wheel(wheel_values):
    random_number=random.randint(0,len(wheel_values)-1)
    return wheel_values[random_number]


#randomly chosen wheel_puzzle from the wheel_puzzles list
def choose_puzzle(wheel_puzzles):
    random_number=random.randint(0,len(wheel_puzzles)-1)
    return wheel_puzzles[random_number]

#judge if the user_guess is in the string
def is_guess_in_puzzle(user_guess,puzzle):
    if user_guess in puzzle:
        return True
    else:
        return False


#compute player's score of each round
def compute_player_score(number_of_times_letter_is_in_puzzle,spin_value):
    score=number_of_times_letter_is_in_puzzle*int(spin_value)
    return score


#changes a puzzle from letters to underscores
def change_to_underscore_puzzle(puzzle):
    intab = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
    outtab = "____________________________________________________ "
    trantab = maketrans(intab, outtab)
    return puzzle.translate(trantab)



#do not call this function
def get_index_list(user_guess, puzzle, blank_puzzle):
    index_list = list()
    index = 0
    for letter in puzzle:
        if letter == user_guess:
            index_list.append(index)
        index += 1

    return index_list


#do not call this function
def swap_letters(user_guess, puzzle, blank_puzzle, index_list):
    index = 0
    blank_puzzle_list = list(blank_puzzle)
    for letter in blank_puzzle_list:
        if index in index_list:
            blank_puzzle_list[index] = user_guess

        index += 1

    return blank_puzzle_list


#this function replaces underscores with the correct user_guess
def transform_puzzle(user_guess, puzzle, blank_puzzle):
    index_list = get_index_list(user_guess, puzzle, blank_puzzle)
    transformed_puzzle = swap_letters(user_guess, puzzle, blank_puzzle, index_list)
    return transformed_puzzle


# plays the game until the user solves the puzzle or all the letters are guessed
def play_game(under_score_puzzle,puzzle,wheel_values):
    player1=Player(raw_input("Player 1 please enter your name: "),0)
    player2=Player(raw_input("Player 2 please enter your name: "),0)
    player3=Player(raw_input("Player 3 please enter your name: "),0)

    turn_number=0 #a variable represents which player should play the game
    current_player=""  #a variable shows the player which is playing the wheel
    current_score=0    #shows current player's score
    puzzle_with_underscores_and_letters=under_score_puzzle
    sign_of_ending=0 # if a player gives the right solution or all the letters have been guessed, this variable equals to 1
    user_guesses=list()
    while(puzzle_with_underscores_and_letters!=puzzle):
        turn_number+=1 # when switching a player, the turn_number would plus one
        # update current player's name and his score
        if turn_number%3==1:
            current_player=player1.name
            current_score=player1.score
        elif turn_number%3==2:
            current_player=player2.name
            current_score=player2.score
        else:
            current_player=player3.name
            current_score=player3.score

        print current_player
        print "The puzzle is",puzzle_with_underscores_and_letters
        print "You have",current_score,"dollars"
        spin_value=0
        while(spin_value!="-1")and(spin_value!="-2"):
            choice=raw_input("What would you like to do Spin (spin) or Solve (solve): ")
            choice=choice.lower() #transfer users' input to all lower letters
            # choose spin
            if choice=="spin":
                spin_value=spin_wheel(wheel_values)
                if spin_value=="-1":
                    print "Your spin is: Bankrupt."
                    print "You lose and your turn."
                    break
                elif spin_value=="-2":
                    print "Your spin is: Lose Turn."
                    print "You lose and your turn."
                    break
                else:
                    print "Your spin is:",spin_value
                    user_guess=raw_input("Please guess a vowel or a consonant: ")
                    if user_guess in user_guesses: # check if the letter has already been guesses
                        print "Your letter",user_guess,"has already been guessed."
                        break
                    else:
                        user_guesses.append(user_guess) # store users' guesses in a list
                        if (is_guess_in_puzzle(user_guess,puzzle)):
                            number_of_times_letter_is_in_puzzle=puzzle.count(user_guess)
                            current_score+=compute_player_score(number_of_times_letter_is_in_puzzle,spin_value)
                            puzzle_with_underscores_and_letters=transform_puzzle(user_guess,puzzle,puzzle_with_underscores_and_letters)
                            puzzle_with_underscores_and_letters="".join(puzzle_with_underscores_and_letters)
                            if puzzle_with_underscores_and_letters==puzzle: # the condition that all the letters in the puzzle have been guesses
                                print "You have guesses all the letters. You win!"
                                sign_of_ending=1 # game ends
                                print "The puzzle is",puzzle_with_underscores_and_letters
                                print "You have",current_score,"dollars"
                                break
                            print current_player
                            print "The puzzle is",puzzle_with_underscores_and_letters
                            print "You have",current_score,"dollars"
                        else:
                            print "Your letter is not in the puzzle."
                            break
            elif choice=="solve":
                solution=raw_input("Please enter the letters of the puzzle: ")
                if (solution==puzzle):
                    sign_of_ending=1
                    print "You win!"
                    print "You won",current_score,"dollars"
                    break
                else:
                    print "You have got the wrong solution."
                    break
        if sign_of_ending==1:
            break
        if turn_number%3==1:
            player1.score+=current_score
        elif turn_number%3==2:
            player2.score+=current_score
        else:
            player3.score+=current_score




# main function
def main():
	 # read information from file
    wheel_values = read_wheel_values()
    wheel_puzzles = read_wheel_puzzles()

    #randomly choose a puzzle
    puzzle=choose_puzzle(wheel_puzzles)
    # call the change_to_underscore_puzzle(puzzle) function to change the puzzle to underscores
    #example: underscore_puzzle = change_to_underscore_puzzle(puzzle)
    underscore_puzzle=change_to_underscore_puzzle(puzzle)
    #call the play_game function to play the game
    #example:  play_game(underscore_puzzle, puzzle, wheel_values)
    play_game(underscore_puzzle,puzzle,wheel_values)



main()


