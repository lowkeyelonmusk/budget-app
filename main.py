import math

class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.balance = 0

    def deposit(self, amount, description=""):
        self.ledger.append({ "amount": amount, "description": description, })
        self.balance += amount

    def withdraw(self, amount, description=""):
        state = self.check_funds(amount)
        if state:
            self.ledger.append({ "amount": 0 - amount, "description": description, })
            self.balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount, category):
        state = self.check_funds(amount)
        if state:
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
        return state
    
    def check_funds(self, amount):
        return amount <= self.balance

    def __str__(self):
        length = len(self.name)
        firsthalf = math.floor((30 - length) / 2)
        secondhalf = 30 - length - firsthalf
        title = f"{'*' * firsthalf}{self.name}{'*' * secondhalf}\n"
        if not self.ledger:
            return "No transactions yet."
        body = ""
        for item in self.ledger:
            amount = item["amount"]
            description = item["description"]

            form_amount = f"{amount:.2f}"
            form_desc = description[:23]
            title += f"{form_desc:<23}{form_amount:>7}\n"
        title += f"Total: {self.balance:.2f}"
        return title

def create_spend_chart(categories):
    title = "Percentage spent by category"
    content = []
    data = {}
    total = 0
    for cat in categories:
        for transaction in cat.ledger:
            if transaction["amount"] < 0:
                amount = -transaction["amount"]
                data[cat.name] = data.get(cat.name, 0) + amount
                total += amount

    elements = 0
    longest = ""
    for item in data:
        elements += 1
        if len(item) > len(longest):
            longest = item
        calc = (data[item] / total) * 100
        data[item] = int(calc // 10) * 10
        

    required = 3 * elements + 1
    print(data)
    for i in range(100, -1, -10):
        size = " " * (3 - len(str(i)))
        row = size + f"{i}|"
        fillers = ""
        for cat in categories:
            if data.get(cat.name, 0) >= i:
                row += " o "
            else:
                row += "   "
        content.append(row + " ")

    content.append("    " + "-" * (len(categories) * 3 + 1))

    for i in range(len(longest)):
        temp = "    "
        
        for cat in categories:
            if i < len(cat.name):
                temp += " " + cat.name[i] + " "
            else:
                temp += "   "
        content.append(temp + " ") 
    
    return title + "\n" + "\n".join(content)

food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")

clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55, "t-shirt")

print(food)
print("\n" + create_spend_chart([food, clothing]))