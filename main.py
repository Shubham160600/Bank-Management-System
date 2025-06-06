import pickle
import os
import pathlib

class Account:
    def __init__(self):
        self.accNo = 0
        self.name = ''
        self.deposit = 0
        self.type = ''
    
    def createAccount(self):
        while True:
            try:
                self.accNo = int(input("Enter the account no: "))
                if self.accNo <= 0:
                    print("Account number must be positive!")
                    continue
                break
            except ValueError:
                print("Please enter a valid account number!")
        
        self.name = input("Enter the account holder name: ").strip()
        while not self.name:
            print("Name cannot be empty!")
            self.name = input("Enter the account holder name: ").strip()
        
        while True:
            self.type = input("Enter the type of account [C/S]: ").upper().strip()
            if self.type in ['C', 'S']:
                break
            print("Please enter 'C' for Current or 'S' for Savings!")
        
        min_amount = 1000 if self.type == 'C' else 500
        while True:
            try:
                self.deposit = int(input(f"Enter the initial amount (>={min_amount} for {'Current' if self.type == 'C' else 'Savings'}): "))
                if self.deposit >= min_amount:
                    break
                print(f"Minimum amount required is {min_amount}!")
            except ValueError:
                print("Please enter a valid amount!")
        
        print("\nAccount Created Successfully!")
    
    def showAccount(self):
        print(f"Account Number: {self.accNo}")
        print(f"Account Holder Name: {self.name}")
        print(f"Type of Account: {'Current' if self.type == 'C' else 'Savings'}")
        print(f"Balance: {self.deposit}")
    
    def modifyAccount(self):
        print(f"Account Number: {self.accNo}")
        
        new_name = input("Modify Account Holder Name: ").strip()
        if new_name:
            self.name = new_name
        
        while True:
            new_type = input("Modify type of Account [C/S]: ").upper().strip()
            if new_type in ['C', 'S', '']:
                if new_type:
                    self.type = new_type
                break
            print("Please enter 'C' for Current or 'S' for Savings!")
        
        while True:
            try:
                new_deposit = input("Modify Balance: ").strip()
                if new_deposit:
                    self.deposit = int(new_deposit)
                    if self.deposit < 0:
                        print("Balance cannot be negative!")
                        continue
                break
            except ValueError:
                print("Please enter a valid amount!")
    
    def depositAmount(self, amount):
        self.deposit += amount
    
    def withdrawAmount(self, amount):
        if amount <= self.deposit:
            self.deposit -= amount
            return True
        return False
    
    def report(self):
        print(f"{self.accNo:>10} {self.name:>20} {self.type:>10} {self.deposit:>15}")
    
    def getAccountNo(self):
        return self.accNo
    
    def getAccountHolderName(self):
        return self.name
    
    def getAccountType(self):
        return self.type
    
    def getDeposit(self):
        return self.deposit

def intro():
    print("\t\t\t\t**********************")
    print("\t\t\t\tBANK MANAGEMENT SYSTEM")
    print("\t\t\t\t**********************")
    input("Press Enter to continue...")

def checkAccountExists(accNo):
    """Check if account number already exists"""
    file = pathlib.Path("accounts.data")
    if file.exists():
        try:
            with open('accounts.data', 'rb') as infile:
                mylist = pickle.load(infile)
                for item in mylist:
                    if item.accNo == accNo:
                        return True
        except:
            pass
    return False

def writeAccount():
    account = Account()
    account.createAccount()
    
    # Check if account number already exists
    if checkAccountExists(account.accNo):
        print("Account number already exists! Please use a different account number.")
        return
    
    writeAccountsFile(account)

def displayAll():
    file = pathlib.Path("accounts.data")
    if file.exists():
        try:
            with open('accounts.data', 'rb') as infile:
                mylist = pickle.load(infile)
                if not mylist:
                    print("No records to display")
                    return
                
                print(f"{'Account No':>10} {'Name':>20} {'Type':>10} {'Balance':>15}")
                print("-" * 55)
                for item in mylist:
                    item.report()
        except Exception as e:
            print(f"Error reading accounts file: {e}")
    else:
        print("No records to display")

def displaySp(num): 
    file = pathlib.Path("accounts.data")
    if file.exists():
        try:
            with open('accounts.data', 'rb') as infile:
                mylist = pickle.load(infile)
                
            found = False
            for item in mylist:
                if item.accNo == num:
                    print(f"Your account balance is: {item.deposit}")
                    found = True
                    break
            
            if not found:
                print("No existing record with this account number")
        except Exception as e:
            print(f"Error reading accounts file: {e}")
    else:
        print("No records to search")

def depositAndWithdraw(num1, num2): 
    file = pathlib.Path("accounts.data")
    if not file.exists():
        print("No records to search")
        return
    
    try:
        with open('accounts.data', 'rb') as infile:
            mylist = pickle.load(infile)
        
        found = False
        for item in mylist:
            if item.accNo == num1:
                found = True
                if num2 == 1:  # Deposit
                    while True:
                        try:
                            amount = int(input("Enter the amount to deposit: "))
                            if amount > 0:
                                item.depositAmount(amount)
                                print("Your account has been updated")
                                break
                            else:
                                print("Amount must be positive!")
                        except ValueError:
                            print("Please enter a valid amount!")
                            
                elif num2 == 2:  # Withdraw
                    while True:
                        try:
                            amount = int(input("Enter the amount to withdraw: "))
                            if amount > 0:
                                if item.withdrawAmount(amount):
                                    print("Your account has been updated")
                                else:
                                    print("Insufficient balance!")
                                break
                            else:
                                print("Amount must be positive!")
                        except ValueError:
                            print("Please enter a valid amount!")
                break
        
        if not found:
            print("No existing record with this account number")
            return
        
        # Write back to file
        with open('accounts.data', 'wb') as outfile:
            pickle.dump(mylist, outfile)
            
    except Exception as e:
        print(f"Error processing transaction: {e}")

def deleteAccount(num):
    file = pathlib.Path("accounts.data")
    if not file.exists():
        print("No records to search")
        return
    
    try:
        with open('accounts.data', 'rb') as infile:
            oldlist = pickle.load(infile)
        
        newlist = [item for item in oldlist if item.accNo != num]
        
        if len(newlist) == len(oldlist):
            print("No existing record with this account number")
            return
        
        with open('accounts.data', 'wb') as outfile:
            pickle.dump(newlist, outfile)
        
        print("Account deleted successfully")
        
    except Exception as e:
        print(f"Error deleting account: {e}")
     
def modifyAccount(num):
    file = pathlib.Path("accounts.data")
    if not file.exists():
        print("No records to search")
        return
    
    try:
        with open('accounts.data', 'rb') as infile:
            mylist = pickle.load(infile)
        
        found = False
        for item in mylist:
            if item.accNo == num:
                found = True
                print("\nCurrent Account Details:")
                item.showAccount()
                print("\nEnter new details (press Enter to keep current value):")
                item.modifyAccount()
                print("Account modified successfully")
                break
        
        if not found:
            print("No existing record with this account number")
            return
        
        with open('accounts.data', 'wb') as outfile:
            pickle.dump(mylist, outfile)
            
    except Exception as e:
        print(f"Error modifying account: {e}")

def writeAccountsFile(account): 
    file = pathlib.Path("accounts.data")
    oldlist = []
    
    if file.exists():
        try:
            with open('accounts.data', 'rb') as infile:
                oldlist = pickle.load(infile)
        except:
            oldlist = []
    
    oldlist.append(account)
    
    try:
        with open('accounts.data', 'wb') as outfile:
            pickle.dump(oldlist, outfile)
        print("Account saved successfully!")
    except Exception as e:
        print(f"Error saving account: {e}")

def getValidChoice():
    """Get valid menu choice from user"""
    while True:
        try:
            choice = input("Select Your Option (1-8): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                return choice
            else:
                print("Invalid choice! Please enter a number between 1-8.")
        except:
            print("Invalid input! Please try again.")

def getValidAccountNumber():
    """Get valid account number from user"""
    while True:
        try:
            num = int(input("Enter the account number: "))
            if num > 0:
                return num
            else:
                print("Account number must be positive!")
        except ValueError:
            print("Please enter a valid account number!")

# Start of the program
def main():
    intro()
    
    while True:
        print("\n" + "="*50)
        print("\tMAIN MENU")
        print("="*50)
        print("\t1. NEW ACCOUNT")
        print("\t2. DEPOSIT AMOUNT")
        print("\t3. WITHDRAW AMOUNT")
        print("\t4. BALANCE ENQUIRY")
        print("\t5. ALL ACCOUNT HOLDER LIST")
        print("\t6. CLOSE AN ACCOUNT")
        print("\t7. MODIFY AN ACCOUNT")
        print("\t8. EXIT")
        print("="*50)
        
        ch = getValidChoice()
        
        if ch == '1':
            writeAccount()
        elif ch == '2':
            num = getValidAccountNumber()
            depositAndWithdraw(num, 1)
        elif ch == '3':
            num = getValidAccountNumber()
            depositAndWithdraw(num, 2)
        elif ch == '4':
            num = getValidAccountNumber()
            displaySp(num)
        elif ch == '5':
            displayAll()
        elif ch == '6':
            num = getValidAccountNumber()
            deleteAccount(num)
        elif ch == '7':
            num = getValidAccountNumber()
            modifyAccount(num)
        elif ch == '8':
            print("\nThanks for using Bank Management System!")
            break
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
