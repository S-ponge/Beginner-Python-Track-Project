import random

def split_bill(_people, bill, lucky=False):
    i = len(_people)
    if lucky:
        i -= 1
        keys = list(_people.keys())
        lucky_one = random.choice(keys)
        print(f"\n{lucky_one} is the lucky one!\n")
        for person in _people:
            if person != lucky_one:
                _people[person] = round(final_bill / i, 2)
    else:
        for person in _people:
            _people[person] = round(final_bill / i, 2)
    return _people


people = {}
i = int(input("Enter the number of friends joining (including you):\n"))
if i <= 0:
    print("No one is joining for the party\n")
else:
    print("\nEnter the name of every friend (including you), each on a new line: \n")
    for x in range(i):
        name = input()
        people[name] = 0
    final_bill = int(input("Enter the total bill value: \n"))
    use_lucky = input('\nDo you want to use the "Who is lucky?" feature? Write Yes/No:\n')
    if use_lucky == "Yes":
        people = split_bill(people, final_bill, lucky=True)
    else:
        print("\nNo one is going to be lucky\n")
        people = split_bill(people, final_bill)
    print(people)