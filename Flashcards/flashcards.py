import argparse
import random
from io import StringIO
from os.path import exists as file_exists


def add_card():
    log_print(f"The card:")
    term = input()
    log_print(term, False)
    while True:
        dupe_card = find_card(term, True)
        if dupe_card is None:
            break
        else:
            log_print(f'The term "{term}" already exists. Try again:')
            term = input()
            log_print(term, False)
    log_print(f"The definition of the card:")
    definition = input()
    log_print(definition, False)
    while True:
        dupe_card = find_card(definition)
        if dupe_card is None:
            cards[term] = [definition, 0]
            log_print(f'The pair ("{term}":"{definition}") has been added.')
            break
        else:
            log_print(f'The definition "{definition}" already exists. Try again:')
            definition = input()
            log_print(definition, False)


def remove_card():
    log_print("Which Card?")
    term = input()
    log_print(term, False)
    found_card = find_card(term, True)
    if found_card:
        del cards[term]
        log_print("The card has been removed.")
    else:
        log_print(f"Can't remove \"{term}\": there is no such card.")


def import_cards(initialize=False):
    log_print("File name:")
    name = args.import_from if initialize else input()
    if name is not None:
        log_print(name, False)
        if file_exists(name):
            with open(name, "r") as file:
                loaded_cards = file.readlines()
                for card in loaded_cards:
                    card = card.replace("\n", "")
                    term, definition, mistakes = card.split(":")
                    cards[term] = [definition, int(mistakes)]
            log_print(f"{len(loaded_cards)} cards have been loaded.")
        else:
            log_print("File not found.")


def export_cards(save_quit=False):
    log_print("File name:")
    name = args.export_to if save_quit else input()
    if name is not None:
        log_print(name, False)
        with open(name, "w") as file:
            for k, v in cards.items():
                file.write(f"{k}:{v[0]}:{v[1]}\n")
        log_print(f"{len(cards)} cards have been saved.")


def ask_card():
    log_print("How many times to ask?")
    count = int(input())
    log_print(count, False)
    for x in range(count):
        term = random.choice(list(cards))
        definition = cards[term][0]
        log_print(f'Print the definition of "{term}":')
        answer = input()
        log_print(answer, False)
        if definition == answer:
            log_print("Correct!")
        else:
            cards[term][1] += 1
            other_term = find_card(answer)
            if other_term is None or other_term == term:
                other_term = "."
            else:
                if answer == "???":
                    definition = other_term
                    other_term = "."
                else:
                    other_term = f', but your definition is correct for "{other_term}".'
            log_print(f'Wrong. The right answer is "{definition}"{other_term}')


def find_card(text, term=False):
    card = None
    for k, v in cards.items():
        if term:
            if text == k:
                card = k
        else:
            if text == v[0]:
                card = k
    return card


def hardest_card():
    hard_cards = []
    error = 0
    for k, v in cards.items():
        if v[1] > error:
            error = v[1]
            hard_cards.clear()
            hard_cards.append(k)
        elif v[1] == error:
            hard_cards.append(k)
    if error > 0:
        if len(hard_cards) == 1:
            log_print(f'The hardest card is {hard_cards[0]}. You have {error} errors answering it.')
        else:
            text = ", ".join(['"{0}"'.format(x) for x in hard_cards])
            log_print(f"The hardest card are {text}. You have {error} errors answering them.")
    else:
        log_print("There are no cards with errors.")


def reset_stats():
    for k in cards.keys():
        cards[k][1] = 0
    log_print("Card statistics have been reset.")


def log_print(text, do_print=True):
    text = str(text)
    log_file.write(text + "\n")
    if do_print:
        print(text)


def save_log():
    log = log_file.getvalue()
    log_print("File name:")
    name = input()
    log_print(name, False)
    with open(name, "w") as file:
        file.write(log)
    log_print("The log has been saved.")


parse = argparse.ArgumentParser()
parse.add_argument("--import_from")
parse.add_argument("--export_to")

args = parse.parse_args()
if __name__ == "__main__":
    log_file = StringIO()
    cards = {}
    import_cards(True)
    i_text = "\nInput the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):"
    while True:
        log_print(i_text)
        i = input()
        log_print(i, False)
        if i == "add":
            add_card()
        elif i == "remove":
            remove_card()
        elif i == "import":
            import_cards()
        elif i == "export":
            export_cards()
        elif i == "ask":
            ask_card()
        elif i == "log":
            save_log()
        elif i == "hardest card":
            hardest_card()
        elif i == "reset stats":
            reset_stats()
        elif i == "exit":
            export_cards(True)
            log_print("Bye bye!")
            break
