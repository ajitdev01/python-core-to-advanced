class BalanceError(Exception):
    pass

def withdraw(balance):
    if balance < 500:
        raise BalanceError("Insufficient balance")
    print("Withdrawal successful")

try:
    withdraw(300)
except BalanceError as e:
    print(e)
