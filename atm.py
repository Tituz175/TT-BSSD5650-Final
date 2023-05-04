from bank import Bank


class Atm(Bank):
    def __init__(self):
        super().__init__()
        self.signin()

    def signin(self):
        print("Welcome to First Bank.\n 1.Create an account. \n 2.Log in to your account.")
        choice = int(input("Select an option: "))
        if choice == 1:
            print("1.\tSavings Account\n2.\tCurrent Account")
            choice = int(input("Select an option "))
            if choice == 1:
                self.openAccount(self.savingsAccount())
            elif choice == 2:
                self.openAccount(self.currentAccount())
            else:
                print("Sorry, Invalid selection")
                return
            choice = int(input("Select an option "))
            if choice == 1:
                access, userId = self.login()
                if access:
                    self.userDashboard(userId)
                else:
                    print("\nSorry, Your login details are invalid.")
                    return
            else:
                print(f"Bye {self.firstName}, have a nice.")
            return
        elif choice == 2:
            access, userId = self.login()
            if access:
                self.userDashboard(userId)
            else:
                print("\nSorry, Your login details are invalid.")
                return
