class Transaction:
    def __init__(self, input: str, output: str, amount: float, signature = None):
        self.input = input
        self.output = output
        self.amount = amount
        self.signature = signature