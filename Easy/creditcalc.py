import math
import argparse

def number_of_monthly_payment(principal, payment, interest):
    i = interest / (12 * 100)
    n = math.ceil(math.log((payment / (payment - i * principal)), 1 + i))
    paid = n * payment
    overpaid = math.floor(paid - principal)
    year = ""
    month = ""
    x = int(n % 12)
    y = int(n / 12)
    if x == 1:
        month = "1 month "
    elif n % 12 > 1:
        month = str(math.ceil(x)) + " months "
    if y == 1:
        year = "1 year "
    elif y > 1:
        year = str(round(y)) + " years "
    print(f"It will take {year}and {month}to repay this loan!")
    print(f"\nOverpayment = {overpaid}")

def annuity_monthly_payment(principal, number_of_periods, interest):
    i = interest / (12 * 100)
    payment = math.ceil(principal * (i * (1 + i) ** number_of_periods) / ((1 + i) ** number_of_periods - 1))
    paid = payment * number_of_periods
    overpaid = math.ceil(paid - principal)
    print(f"Your monthly payment = {payment}!")
    print(f"\nOverpayment = {overpaid}")

def differentiated_monthly_payment(principal, number_of_periods, interest):
    i = interest / (12 * 100)
    paid = 0
    for m in range(1, int(number_of_periods) + 1):
        payment = math.ceil(principal / number_of_periods + i * (principal - ((principal * (m - 1)) / number_of_periods)))
        paid += payment
        print(f"Month {m}: payment is {payment}")
    overpaid = math.floor(paid - principal)
    print(f"\nOverpayment = {overpaid}")

def principal_calculation(annuity, number_of_periods, interest):
    i = interest / (12 * 100)
    principal = math.floor(annuity / ((i * (1 + i) ** number_of_periods) / ((1 + i) ** number_of_periods - 1)))
    paid = annuity * number_of_periods
    overpaid = math.floor(paid - principal)
    print(principal)
    print(f"\nOverpayment = {overpaid}")

def incorrect():
    print("Incorrect parameters.")

parser = argparse.ArgumentParser()
parser.add_argument("--type", choices=["annuity", "diff"])
parser.add_argument("--principal")
parser.add_argument("--payment")
parser.add_argument("--periods")
parser.add_argument("--interest")

args = parser.parse_args()
args_list = [args.type, args.principal, args.payment, args.periods, args.interest]
args_count = 0
negative_amount = False

for i in range(len(args_list)):
    if args_list[i] is not None:
        if i > 0:
            args_list[i] = float(args_list[i])
            if args_list[i] < 0:
                negative_amount = True
    else:
        args_count += 1

if args_count > 1:
    incorrect()
if args_list[0] is None:
    incorrect()
elif args_list[4] is None:
    incorrect()
elif negative_amount is True:
    incorrect()
else:
    if args.type == "diff":
        differentiated_monthly_payment(args_list[1], args_list[3], args_list[4])
    else:
        if args_list[1] is None:
            principal_calculation(args_list[2], args_list[3], args_list[4])
        elif args_list[2] is None:
            annuity_monthly_payment(args_list[1], args_list[3], args_list[4])
        elif args_list[3] is None:
            number_of_monthly_payment(args_list[1], args_list[2], args_list[4])
