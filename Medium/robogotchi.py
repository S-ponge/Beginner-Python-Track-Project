import random


class Robot:
    def __init__(self, name):
        self.name = name
        self.battery = 100
        self.overheat = 0
        self.skill = 0
        self.boredom = 0
        self.rust = 0

    def get_info(self):
        text = (f"\n{self.name}'s stats are: battery is {self.battery},\n"
                f"overheat is {self.overheat},\n"
                f"skill level is {self.skill},\n"
                f"boredom is {self.boredom},\n"
                f"rust is {self.rust}.")
        return text

    def change_battery(self, value=0, reset=False):
        old_val = self.battery
        if reset:
            self.battery = 100
        else:
            self.battery += value
        if self.battery == 100:
            if old_val != 100:
                print(f"{self.name} is recharged!")
        else:
            print(f"{self.name}'s level of the battery was {old_val}. Now it is {self.battery}.")

    def change_overheat(self, value=0, reset=False):
        old_val = self.overheat
        if reset:
            self.overheat = 0
        else:
            self.overheat += value
        if self.overheat < old_val:
            print(f"{self.name} cooled off")
            if self.overheat < 0:
                self.overheat = 0
        elif self.overheat == 100:
            print(f"The level of overheat reached 100, {self.name} has blown up! Game over. Try again?")
            return True
        print(f"{self.name}'s level of overheat was {old_val}. Now it is {self.overheat}.")
        return False

    def change_skill(self, value=0, reset=False):
        old_val = self.skill
        if reset:
            self.skill = 0
        else:
            self.skill += value
        if self.skill == 0:
            if old_val != 0:
                print(f"{self.name} cooled off!")
            else:
                print(f"{self.name} cool!")
        else:
            print(f"{self.name}'s level of skill was {old_val}. Now it is {self.skill}.")

    def change_boredom(self, value=0, reset=False):
        old_val = self.boredom
        if reset:
            self.boredom = 0
        else:
            self.boredom += value
        if self.boredom < 0:
            self.boredom = 0
        print(f"{self.name}'s level of boredom was {old_val}. Now it is {self.boredom}.")

    def change_rust(self, value=0, reset=False):
        extra_text = ["", f"{self.name} is less rusty!"]
        old_val = self.rust
        if reset:
            self.rust = 0
        else:
            self.rust += value
        if self.rust < 0:
            self.rust = 0
        elif self.rust >= 100:
            print(f"{self.name} is too rusty! Game over. Try again?")
            return True
        print(f"{self.name}'s level of rust was {old_val}. Now it is {self.rust}. "
              f"{extra_text[0] if value >= 0 else extra_text[1]}")
        return False


def number_game():
    player_wins = 0
    robots_wins = 0
    draws = 0

    while True:
        x = input("What is your number?")
        goal = random.randint(0, 1000000)
        robot_number = random.randint(0, 1000000)
        try:
            if x.lstrip("-").isdigit():
                x = int(x)
                assert x < 1000000, "Invalid input! The number can't be bigger than 1000000."
                assert x >= 0, "The number can't be negative!"
                a = abs(goal - x)
                b = abs(goal - robot_number)
                print(f"\nThe robot entered the number {robot_number}.")
                print(f"The goal number is {goal}.")
                if a < b:
                    player_wins += 1
                    print("You won!")
                elif b < a:
                    robots_wins += 1
                    print("The robot won!")
                else:
                    draws += 1
                    print("It's a draw!")
                print(f"\nYou won: {player_wins},\nRobot won: {robots_wins},\nDraws: {draws}.\n")
            else:
                assert x == "exit game", "A string is not a valid input!"
                print(f"\nYou won: {player_wins},\nRobot won: {robots_wins},\nDraws: {draws}.\n")
                return False
        except (AssertionError) as err:
            print(err)


def rock_paper_scissors_game():
    player_wins = 0
    robots_wins = 0
    draws = 0

    moves = ["rock", "paper", "scissors"]
    while True:
        x = input("What is your move?")
        robot_move = random.randint(0, 2)
        try:
            if x in moves:
                print(f"The robot chose {moves[robot_move]}")
                if moves[robot_move] == x:
                    draws += 1
                    print("It's a draw!")
                elif moves[robot_move - 1] == x:
                    robots_wins += 1
                    print("The robot won!")
                else:
                    player_wins += 1
                    print("You won!")
            else:
                assert x == "exit game", "No such option! Try again!"
                print(f"\nYou won: {player_wins},\nRobot won: {robots_wins},\nDraws: {draws}.\n")
                return False
        except (AssertionError) as err:
            print(err)


def bad_event(_robot):
    if _robot.battery > 30:
        return False
    elif _robot.battery <= 10:
        print(f"Guess what! {_robot.name} fell into the pool!")
        _too_rusty = _robot.change_rust(50)
    elif _robot.battery <= 30:
        print(f"Oh no, {_robot.name} stepped into a puddle!")
        _too_rusty = _robot.change_rust(10)
    return _too_rusty


quit = False
name = input("How will you call your robot?")
robot = Robot(name)
a = f"\nAvailable interactions with {robot.name}:"

interactions = """exit - Exit
info - Check the vitals
work - Work
play - Play
oil - Oil
recharge - Recharge
sleep - Sleep mode
learn - Learn skills"""

while quit is not True:
    print(a)
    print(interactions)
    interaction = input("Choose:\n").lower()
    if interaction == "info":
        print(robot.get_info())
    elif interaction == "recharge":
        if robot.battery == 100:
            print(f"{robot.name} is charged!")
        else:
            robot.change_overheat(-5)
            robot.change_boredom(5)
            robot.change_battery(10)
            print(f"{robot.name} is recharged")
    if robot.battery == 0:
        print(f"The level of the battery is 0, {robot.name} needs recharging!")
    else:
        if interaction == "play":
            playing = True
            i = input("Which game would you like to play?").lower()
            while playing:
                if i == "numbers":
                    state = number_game()
                    robot.change_boredom(-20)
                    quit = robot.change_overheat(10)
                    if robot.boredom == 0:
                        print(f"{robot.name} is in a great mood!")
                    playing = state
                elif i == "rock-paper-scissors":
                    state = rock_paper_scissors_game()
                    robot.change_boredom(-20)
                    quit = robot.change_overheat(10)
                    if robot.boredom == 0:
                        print(f"{robot.name} is in a great mood!")
                    playing = state
                else:
                    i = input("Please choose a valid option: Numbers or Rock-paper-scissors?").lower()
        elif robot.boredom == 100:
            print(f"{robot.name} is too bored! {robot.name} needs to have fun!")
        else:
            if interaction == "sleep":
                robot.change_overheat(-20)
                if robot.overheat == 0:
                    print(f"{robot.name} is cool")
            elif interaction == "learn":
                if robot.skill == 100:
                    print(f"There's nothing for {robot.name} to learn!")
                else:
                    too_rusty = bad_event(robot)
                    if too_rusty:
                        quit = True
                    else:
                        print("")
                        robot.change_skill(10)
                        quit = robot.change_overheat(10)
                        robot.change_battery(-10)
                        robot.change_boredom(5)
                        print("")
                        print(f"{robot.name} has become smarter!")
            elif interaction == "work":
                if robot.skill < 50:
                    print(f"{robot.name} has got to learn before working!")
                else:
                    too_rusty = bad_event(robot)
                    if too_rusty:
                        quit = True
                    else:
                        quit = robot.change_overheat(10)
                        robot.change_battery(-10)
                        robot.change_boredom(10)
                        print(f"{robot.name} did well!")
            elif interaction == "oil":
                if robot.rust == 0:
                    print(f"{robot.name} is fine, no need to oil!")
                else:
                    robot.change_rust(-20)
            elif interaction == "exit":
                print("Game over")
                quit = True
            else:
                print("Invalid input, try again!")

