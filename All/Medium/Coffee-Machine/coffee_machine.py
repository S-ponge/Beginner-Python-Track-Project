def print_state(_money, cups, _available_amount):
    text = "\nThe coffee machine has:\
 \n{} ml of water\
 \n{} ml of milk\
 \n{} g of coffee beans\
 \n{} disposable cups\
 \n${} of money\n".format(_available_amount["water"],
                          _available_amount["milk"], _available_amount["coffee"],
                          cups, _money)
    print(text)


def buy(coffee, count, cups, _available_amount, _money):
    can_buy = True
    old_amount = _available_amount
    _message = "I have enough resources, making you a coffee!\n"
    for ingredient in _available_amount:
        amount = coffee[ingredient] * count
        if amount <= _available_amount[ingredient]:
            _available_amount[ingredient] -= amount
        else:
            can_buy = False
            _message = f"Sorry, not enough {ingredient}!\n"
            break
    if can_buy:
        if cups >= count:
            cups -= count
        _money += coffee["price"] * count
    else:
        _available_amount = old_amount
    return cups, _money, _available_amount, _message


def fill(cups, _available_amount):
    a = int(input("Write how many ml of water you want to add: \n"))
    _available_amount["water"] += a
    b = int(input("Write how many ml of milk you want to add: \n"))
    _available_amount["milk"] += b
    c = int(input("Write how many grams of coffee beans you want to add: \n"))
    _available_amount["coffee"] += c
    d = int(input("Write how many cups of coffee you want to add: \n"))
    cups += d
    return cups, _available_amount


def take(_money):
    print(f"\nI gave you ${money}\n")
    _money = 0
    return _money


money = 550
disposable_cups = 9
available_amount = {"water": 400, "milk": 540, "coffee": 120}

espresso = {"water": 250, "milk": 0, "coffee": 16, "price": 4}
latte = {"water": 350, "milk": 75, "coffee": 20, "price": 7}
cappuccino = {"water": 200, "milk": 100, "coffee": 12, "price": 6}

while True:
    i = input("Write action (buy, fill, take, remaining, exit): \n")
    if i == "buy":
        x = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu: \n")
        if x == "back":
            pass
        else:
            x = int(x)
            if x == 1:
                disposable_cups, money, available_amount, message = \
                    buy(espresso, 1, disposable_cups, available_amount, money)
                print(message)
            elif x == 2:
                disposable_cups, money, available_amount, message = \
                    buy(latte, 1, disposable_cups, available_amount, money)
                print(message)
            else:
                disposable_cups, money, available_amount, message = \
                    buy(cappuccino, 1, disposable_cups, available_amount, money)
                print(message)
                print()
    elif i == "fill":
        disposable_cups, available_amount = fill(disposable_cups, available_amount)
    elif i == "take":
        money = take(money)
    elif i == "remaining":
        print_state(money, disposable_cups, available_amount)
    elif i == "exit":
        break
