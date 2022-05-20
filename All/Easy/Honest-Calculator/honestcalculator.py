msg_0 = "Enter an equation"

msg_1 = "Do you even know what numbers are? Stay focused!"

msg_2 = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"

msg_3 = "Yeah... division by zero. Smart move..."

msg_4 = "Do you want to store the result? (y / n):"

msg_5 = "Do you want to continue calculations? (y / n):"

msg_6 = " ... lazy"

msg_7 = " ... very lazy"

msg_8 = " ... very, very lazy"

msg_9 = "You are"

msg_10 = "Are you sure? It is only one digit! (y / n)"

msg_11 = "Don't be silly! It's just one number! Add to the memory? (y / n)"

msg_12 = "Last chance! Do you really want to embarrass yourself? (y / n)"

mem_check_msg = [msg_10, msg_11, msg_12]
def is_one_integer(v):
    if v > -10 and v < 10 and v.is_integer():
        return True
    else:
        return False


def check(v1, v2, v3):
    msg = ""
    if is_one_integer(v1) and is_one_integer(v2):
        msg += msg_6
    if v1 == 1 or v2 == 1 and v3 == "*":
        msg += msg_7
    if v1 == 0 or v2 == 0:
        if v3 == "*" or v3 == "+" or v3 == "-":
            msg += msg_8
    if msg != "":
        msg = msg_9 + msg
        print(msg)


def mem_check(x):
    if is_one_integer(x):
        msg_index = 0
        while True:
            i = input(mem_check_msg[msg_index])
            if i == "y":
                if msg_index < 2:
                    msg_index += 1
                else:
                    return True
            elif i == "n":
                return False
    else:
        return True


def calculate(stored_result=0):
    result = None
    M = float(stored_result)
    i = input(msg_0).split(" ")
    try:
        i[0] = float(i[0]) if i[0] != "M" else M
        i[2] = float(i[2]) if i[2] != "M" else M
    except ValueError:
        print(msg_1)
    else:
        check(i[0], i[2], i[1])
        if i[1] == "*":
            result = i[0] * i[2]
        elif i[1] == "/":
            if i[2] == 0:
                print(msg_3)
            else:
                result = i[0] / i[2]
        elif i[1] == "+":
            result = i[0] + i[2]
        elif i[1] == "-":
            result = i[0] - i[2]
        else:
            print(msg_2)
    if result is not None:
        print(result)
        while True:
            a = input(msg_4)
            if a == "y":
                if mem_check(result):
                    M = result
                break
            elif a == "n":
                break
        b = input(msg_5)
        if b == "y":
            calculate(M)
    else:
        calculate()


calculate()