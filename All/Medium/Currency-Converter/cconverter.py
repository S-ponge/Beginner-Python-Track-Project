import requests
import json


class Converter:

    def __init__(self):
        self.exchange_rates = {}
        self.current_currency = ""
        self.target_currency = ""
        self.amount = 0

    def set_current(self):
        self.current_currency = input("Enter current currency: ")
        self.request_json_rates()

    def set_target(self):
        i = input("Enter target currency, leave blank to exit: ").lower()
        if i == "":
            return False
        self.target_currency = i
        return True

    def set_amount(self):
        i = input("Enter current currency amount, leave blank to exit: ")
        if i == "":
            return False
        self.amount = int(i)
        return True

    def request_json_rates(self):
        r = requests.get(f'http://www.floatrates.com/daily/{self.current_currency}.json')
        self.exchange_rates = json.loads(r.text)

    def check_rates(self):
        print("Checking the cache...")
        if self.target_currency in self.exchange_rates:
            print("Oh! It is in the cache!")
        else:
            print("Sorry, but it is not in the cache!")

    def convert_to_target(self):
        rate = self.exchange_rates[self.target_currency]["rate"]
        total = self.amount * rate
        print(f"You received {round(total, 2)} {self.target_currency.upper()}.")

    def main(self):
        self.set_current()
        while True:
            running = self.set_target()
            if not running:
                break
            running = self.set_amount()
            if not running:
                break
            self.check_rates()
            self.convert_to_target()


if __name__ == "__main__":
    Converter().main()
