from currentaccount import CurrentAccount
from openaccount import *
from savingsaccount import SavingsAccount
import datetime as dt


class Bank(SavingsAccount, CurrentAccount):
    def __init__(self):
        super().__init__()
        self.switchDictionary = {
            1: self.withdrawFunds,
            2: self.transferFunds,
            3: self.userBalance,
            4: self.userHistory,
            5: self.logOut
        }
        self.optionCount = 0

    def openAccount(self, accountType):
        self.accountDetails()
        self.accountType = accountType
        self.saveDetails()
        print("\nAccount created successfully.\nDo you want to login?\n1. Yes\n2. No")

    def queryDb(self, userId, table, *args):
        query = "select"
        for item in range(len(args)):
            if item != len(args) - 1:
                query += f" {args[item]},"
            else:
                query += f" {args[item]}"
        query += f" from {table} where User_id = %s"
        value = userId
        cursor.execute(query, (value,))
        return cursor.fetchone()

    def userDashboard(self, userId):
        result = self.queryDb(userId, "users", "First_Name", "Last_Name")
        functionality = ["Withdraw Fund", "Transfer Fund", "Balance", "History", "Log Out"]
        print(f"\nWelcome {result[0]} {result[1]}.")
        for item in range(len(functionality)):
            print(f"{item + 1}.\t{functionality[item]}")
        choice = int(input("Select an option "))
        self.switchCase(choice, userId)

    def switchCase(self, choice, userId):
        return self.switchDictionary.get(choice, self.default)(userId)

    def logOut(self, userId):
        result = self.queryDb(userId, "users", "First_Name", "Last_Name")
        print(f"\nThank you, {result[0]} {result[1]} for banking with us. Have a nice day.\n")

    def userBalance(self, userId):
        result = self.queryDb(userId, "users", "First_Name", "Last_Name", "Balance")
        print(f"{result[0]} {result[1]} your current balance is #{str(result[2])}.")
        choice = int(input("Do you want to perform another transaction?\n1.Yes\n2.No\nSelect an option "))
        if choice == 1:
            self.userDashboard(userId)
        elif choice == 2:
            self.logOut(userId)
        else:
            return print("Sorry, Invalid selection.")

    def checkAvailableFund(self, userId, amount):
        result = self.queryDb(userId, "users", "Balance", "Minimum_balance")
        if result[0] >= amount > result[1]:
            if result[0] - amount > result[1]:
                return True
        else:
            return False

    def performTransaction(self, userId, amount, receiverId=None):
        myTime, myDate = self.timeFormater()
        result = self.queryDb(userId, "users", "Balance", "First_Name", "Last_Name")
        balance_before = result[0]
        balance_after = result[0] - amount
        query = "update users set Balance = %s where User_id = %s"
        values = (balance_after, userId)
        cursor.execute(query, values)
        db.commit()
        if receiverId is None:
            query = "insert into transactions(User_id, Date, Time, Balance_Before, Debit, Balance_After, Remark, Status)values(%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (
                userId, myDate, myTime, balance_before, amount, balance_after, f" withdrawn #{str(amount)}",
                "Successful")
        else:
            receiverDetails = self.queryDb(receiverId, "users", "First_Name", "Last_Name")
            query = "insert into transactions(User_id, Date, Time, Balance_Before, Receiver_id, Debit, Balance_After, Remark, Status)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (
                userId, myDate, myTime, balance_before, receiverId, amount, balance_after,
                f" transferred #{str(amount)} to {receiverDetails[0]} {receiverDetails[1]}",
                "Successful")
        cursor.execute(query, values)
        db.commit()
        print(f"\n{result[1]} {result[2]}, your transaction was successful.")

    def timeFormater(self):
        generateTime = dt.datetime.now()
        myTime = generateTime.strftime("%I") + ":" + generateTime.strftime("%M") + generateTime.strftime("%p")
        myDate = generateTime.strftime("%d") + "-" + generateTime.strftime("%m") + "-" + generateTime.strftime("%Y")
        return myTime, myDate

    def transaction(self, kind, userId, receiverId=None):
        result = self.queryDb(userId, "users", "First_Name")
        choice = int(input(f"{result[0]}, how much do you want to {kind}?\nInput the amount: "))
        if self.checkAvailableFund(userId, choice):
            if receiverId:
                self.performTransaction(userId, choice, receiverId)
                return choice
            else:
                self.performTransaction(userId, choice)
        else:
            print(f"Insufficient balance, {result[0]}")

    def withdrawFunds(self, userId):
        self.transaction("withdraw", userId)
        choice = int(input("Do you want to perform another transaction\n1.\tYes\n2.\tNo\nSection an option: "))
        if choice == 1:
            self.userDashboard(userId)
        else:
            self.logOut(userId)

    def validateCustomer(self, email):
        query = "select Balance, First_Name, Last_Name, User_id from users where Email = %s"
        value = email
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        if result is not None:
            return True, result
        else:
            return False, 0

    def transferFunds(self, userId):
        email = input("\nKindly input the receiver's E-mail\nRight here: ")
        senderDetails = self.queryDb(userId, "users", "Email", "First_Name, Last_Name")
        if senderDetails[0] == email:
            print("Error, You are sending funds to your account from your account.")
            return self.userDashboard(userId)
        access, result = self.validateCustomer(email)
        if access:
            amount = self.transaction("transfer", userId, result[3])
            myTime, myDate = self.timeFormater()
            query = "insert into transactions(User_id, Date, Time, Balance_Before, Sender_id, Credit, Balance_After, Remark, Status)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (result[3], myDate, myTime, result[0], userId, amount, (result[0] + amount),
                      f" received #{amount} from {senderDetails[1]} {senderDetails[2]}", "Successful")
            cursor.execute(query, values)
            db.commit()
            query = "update users set Balance = %s where Email = %s"
            values = ((result[0] + amount), email)
            cursor.execute(query, values)
            db.commit()
            choice = int(input("Do you want to perform another transaction\n1.\tYes\n2.\tNo\nSection an option: "))
            if choice == 1:
                self.userDashboard(userId)
            else:
                self.logOut(userId)
        else:
            print("Error, consumer not found")
            return self.userDashboard(userId)

    def userHistory(self, userId):
        userName = "select First_Name, Last_Name from users where User_id = %s"
        value = userId
        cursor.execute(userName, (value,))
        output = cursor.fetchone()
        query = "select users.User_id,users.First_Name,users.Last_Name,transactions.Tran_id,transactions.Date,transactions.Time,transactions.Balance_After,transactions.Remark,transactions.Status From transactions inner join users on transactions.User_id=users.User_id where users.User_id = %s"
        value = userId
        cursor.execute(query, (value,))
        result = cursor.fetchall()
        if len(result) == 0:
            print(str(output[0]) + " " + str(output[1]) + ", you do not have any transaction history.")
        else:
            for details in result:
                print(
                    f"\nOn {str(details[4])} exactly {str(details[5])}, you {str(details[1])} {str(details[2])} {str(details[-2])} which was {str(details[-1])}.")
        print(" ")
        return self.userDashboard(userId)

    def default(self, userId):
        if self.optionCount < 2:
            result = self.queryDb(userId, "users", "First_Name")
            print(f"\n{result[0]}, Invalid option")
            self.optionCount += 1
            self.userDashboard(userId)
        else:
            print("Exceeded maximum option limit\n")
            return
