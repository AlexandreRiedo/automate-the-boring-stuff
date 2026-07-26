import random
import shelve
import sys

print("ROCK, PAPER, SCISSORS")

# These variables keep track of the number of wins, losses, and ties.
with shelve.open("rpsData") as f:
    if "wins" not in f:
        f["wins"] = 0
    if "losses" not in f:
        f["losses"] = 0
    if "ties" not in f:
        f["ties"] = 0

    wins, losses, ties = f["wins"], f["losses"], f["ties"]

while True:  # The main game loop.
    print(wins, "Wins,", losses, "Losses,", ties, "Ties")
    while True:  # The player input loop.
        print("Enter your move: (r)ock (p)aper (s)cissors or (q)uit")
        playerMove = input()
        if playerMove == "q":
            sys.exit()  # Quit the program.
        if playerMove == "r" or playerMove == "p" or playerMove == "s":
            break  # Break out of the player input loop.
        print("Type one of r, p, s, or q.")

    # Display what the player chose:
    if playerMove == "r":
        print("ROCK versus...")
    elif playerMove == "p":
        print("PAPER versus...")
    elif playerMove == "s":
        print("SCISSORS versus...")

    # Display what the computer chose:
    randomNumber = random.randint(1, 3)
    computerMove = ""
    if randomNumber == 1:
        computerMove = "r"
        print("ROCK")
    elif randomNumber == 2:
        computerMove = "p"
        print("PAPER")
    elif randomNumber == 3:
        computerMove = "s"
        print("SCISSORS")

    # Display and record the win/loss/tie:
    if playerMove == computerMove:
        print("It is a tie!")
        ties = ties + 1
    elif (
        playerMove == "r"
        and computerMove == "s"
        or playerMove == "p"
        and computerMove == "r"
        or playerMove == "s"
        and computerMove == "p"
    ):
        print("You win!")
        wins = wins + 1
    elif (
        playerMove == "r"
        and computerMove == "p"
        or playerMove == "p"
        and computerMove == "s"
        or playerMove == "s"
        and computerMove == "r"
    ):
        print("You lose!")
        losses = losses + 1

    with shelve.open("rpsData") as f:
        f["wins"], f["losses"], f["ties"] = wins, losses, ties
