# This is a guess the number game.
import random

import pymsgbox

secret_number = random.randint(1, 20)
pymsgbox.alert("I am thinking of a number between 1 and 20.")

# Ask the player to guess 6 times.
for guesses_taken in range(1, 7):
    guess = int(pymsgbox.prompt("Take a guess, input a number.") or -1)

    if guess == -1:
        pymsgbox.alert("You've exited from the game.")
        break
    elif guess < secret_number:
        pymsgbox.alert("Your guess is too low.")
    elif guess > secret_number:
        pymsgbox.alert("Your guess is too high.")
    else:
        pymsgbox.alert("Good job! You got it in " + str(guesses_taken) + " guesses!")
        break  # This condition is the correct guess!
else:
    pymsgbox.alert("Nope. The number was " + str(secret_number))
