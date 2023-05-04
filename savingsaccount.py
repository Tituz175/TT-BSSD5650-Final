from openaccount import *


class SavingsAccount(OpenAccountAbstractClass, ABC):
    def __init__(self):
        super().__init__()

    def savingsAccount(self):
        self.accountType = "Savings"
        return self.accountType

