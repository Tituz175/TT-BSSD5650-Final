from abc import ABC, abstractmethod
import mysql.connector as con

db = con.connect(host="localhost", database="db_atm", username="root", password="")
cursor = db.cursor()


class OpenAccountAbstractClass(ABC):
    def __init__(self):
        self.firstName = None
        self.lastName = None
        self.email = None
        self.phone = None
        self.startingBalance = None
        self.pin = None
        self.confirm = None
        self.accountType = None
        super().__init__()

    def template_method(self):
        self.accountDetails()
        self.savingsAccount()
        self.currentAccount()
        self.saveDetails()
        self.login()

    @abstractmethod
    def savingsAccount(self):
        pass

    @abstractmethod
    def currentAccount(self):
        pass

    def accountDetails(self):
        self.firstName = input("What is your First Name? ")
        self.lastName = input("What is your Last Name? ")
        self.email = input("Please enter your E-mail ")
        self.phone = input("Please enter your Phone number ")
        self.startingBalance = input("Kindly enter your starting balance ")
        self.pin = input("Input desire Pin ")
        self.confirm = input("Please confirm your Pin ")

    def saveDetails(self):
        print("Details saved")
        print(f"{self.firstName}, {self.lastName}, {self.email}, {self.phone}, {self.pin}, {self.accountType}")
        query = "select * from users where Email = %s"
        value = self.email
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        if result is None:
            if self.pin == self.confirm:
                if self.accountType == "Savings":
                    minimumBalance = 0
                else:
                    minimumBalance = 5000
                query = "insert into users(First_Name,Last_Name,Email,Phone,Pin,Account_type,Balance,Minimum_balance)values(%s,%s,%s,%s,%s,%s,%s,%s)"
                values = (
                    self.firstName, self.lastName, self.email, self.phone, self.pin, self.accountType,
                    self.startingBalance, minimumBalance)
                cursor.execute(query, values)
                db.commit()
            else:
                print("\nYou input unmatchable passwords.\nPlease restart the registration again.\n")
                return
        else:
            print("Used Email! Please input a unused Email.")
            print(" ")

    def login(self):
        print("Welcome, we are glad to have you here.")
        login_email = input("Please input your E-mail: ")
        login_pin = input("Please input your Password: ")
        query = "select User_id, Phone, Email, Pin from users where Email = %s and Pin = %s"
        values = (login_email, login_pin)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is not None:
            return True, result[0]
        else:
            return False, 0
