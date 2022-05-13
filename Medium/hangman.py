# Write your code here
import random

words = ["python", "java", "swift", "javascript"]
win_count = 0
loss_count = 0
while True:
    i = input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit:')
    if i == "results":
        print(f"You won: {win_count} times.\nYou lost: {loss_count} times.")
    elif i == "exit":
        break
    elif i == "play":
        word = words[random.randint(0, len(words) - 1)]
        won = False
        attempts = 8
        hint = ""
        guesses = []
        for x in range(len(word)):
            hint += "-"
        while attempts != 0:
            print(hint)
            a = input("Input a letter: ")
            exist = False
            if len(a) != 1:
                print("Please, input a single letter.")
                continue
            elif a.isupper() is True or a.isalpha() is False:
                print("Please, enter a lowercase letter from the English alphabet.")
                continue
            if a in guesses:
                print("You've already guessed this letter.")
                continue
            else:
                guesses.append(a)
                for x in range(len(word)):
                    if word[x] == a:
                        hint = hint[:x] + a + hint[x + 1:]
                        exist = True
                if exist is False:
                    print("That letter doesn't appear in the word.")
                    attempts -= 1
            if "-" not in hint:
                print(f"You guessed the word {word}!")
                won = True
                break
        print("You survived!" if won is True else "You lost!")
        if won is True:
            win_count += 1
        else:
            loss_count += 1
    else:
        continue
