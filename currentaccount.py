from openaccount import *


class CurrentAccount(OpenAccountAbstractClass, ABC):
    def __init__(self):
        super().__init__()

    def currentAccount(self):
        self.accountType = "Current"
        return self.accountType

