import os
import time
import sys
from customer_account import CustomerAccount
from file_parser import FileParser

class UserMenu():

    def clearscreen(self):
        os.system('cls')

    def do_user_menu(self, ds):

        selection = "0"

        while(selection != "8"):
            self.clearscreen()
            selection = self.show_user_menu(ds)

            if(selection not in ["1", "2", "3", "4", "5", "6", "7", "8"]):
                self.clearscreen()
                print(f"Invalid menu option [{selection}]. Press return to try again.")
                input()

        # application is now exiting - write customers accounts list to file
        print("=====================================")
        print("Option 8. Exit ")
        print("=====================================")
        self.scroll_text("Saving changes.......................\n")
        print("====================================")
        file_parser = FileParser()

        file_parser.write_customer_account("cust_accounts.txt", ds.customer_accounts_list)
        self.scroll_text("Saved.\n")
        self.scroll_text("Exiting.............................\n")
        

    #little animation to make it fun
    def scroll_text(self,text):
        for char in str(text):
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)


    def show_user_menu(self, ds):

        print("============================")
        print(" ")
        print("WELCOME TO THE BANK MANAGEMENT APP")
        print(" ")
        print("============================")
        print("Menu options:")
        print("1. Register New Customer Account")
        print("2. Deposit")
        print("3. Withdrawal")
        print("4. View all Accounts")
        print("5. View Specific Account")
        print("6. Transference Between Accounts")
        print("7. Help")
        print("8. Exit\n")
        selection = input("Please choose an option (1-8): ")

        if(selection == "1"):
            print("=====================================")
            print("Option 1. Create new customer account")
            print("=====================================")
            self.create_customer_account(ds)

        elif(selection == "2"):
            print("=====================================")
            print("Option 2. Deposit")
            print("=====================================")
            amount = self.deposit_amount()
            customer_account = self.load_customer_account(input("Enter an account number: "), ds.customer_accounts_list)
            if customer_account == "Account not found":
                self.show_user_menu(ds)
            else:
                self.deposit(customer_account, amount)

        elif(selection == "3"):
            print("=====================================")
            print("Option 3. Withdrawal")
            print("=====================================")
            amount = self.withdrawal_amount()
            customer_account = self.load_customer_account(input("Enter account number: "), ds.customer_accounts_list)
            if customer_account == "Account not found":
                self.show_user_menu(ds)
            else:
                self.withdrawal(customer_account, amount)
        
        elif(selection == "4"):
            print("=====================================")
            print("Option 4. View all accounts")
            print("=====================================")
            self.display_all_accounts(ds)
        
        elif(selection == "5"):
            print("=====================================")
            print("Option 5. Search for account ")
            print("=====================================")
            self.display_specific_account(ds)

        elif(selection == "6"):
            print("=====================================")
            print("Option 6. Transfer Bewtween Accounts ")
            print("=====================================")
            amount = self.transfer_amount()
            account_from = self.load_customer_account(input("Transfer from: \n Enter account number: "), ds.customer_accounts_list)
            if account_from == "Account not found":
                self.show_user_menu(ds)
            else:
                account_to = self.load_customer_account(input("Transfer to: \n Enter account number: "), ds.customer_accounts_list)
                if account_to == "Account not found":
                    self.show_user_menu(ds)
                else:
                    self.transfer(account_from, account_to, amount)
          
        elif(selection == "7"):
            print("=====================================")
            print("Option 7. Online Help ")
            print("=====================================")
            self.help()


        return selection

    def display_all_accounts(self, ds):
        self.clearscreen()
        print("Account No.     Forename     Surname      PPSN        Account_Type      Overdraft      Balance")
        print("=================================================================================================")

        for customer_account in ds.customer_accounts_list:
            print(repr(customer_account))

        print("Return to continue...")
        input()        

    def account_type_menu(self):
        selection = "0"
        print('')
        print("Account options:")
        print("================")
        print("1. Deposit:\n Overdraft facility not available for this type of account. Opening deposit must be €50 or more.\n Type 1 to choose this type of account\n")
        print("2. Current:\n Overdraft facility is available for this type of account. Opening deposit must be €25 or more.\n Type 2 to choose this type of account\n")
        selection = int(input("Please choose an option (1 or 2): "))
        while(not (selection == 1 or selection == 2)):
            selection = int(input("Please choose an option (1 or 2): "))
        if selection == 1:
            print("")
            print("Deposit account selected. You must now deposit a minimum of €50")
            print("")
            return "deposit"
        if selection == 2:
            print("")
            print("Current account selected.")
            return "current"


    def create_customer_account(self, ds):
        balance = False
        forename = self.validate_name(input("Forename: "))
        surname = self.validate_name(input("Surname: "))
        ppsn = self.validate_ppsn(input("Enter the PPSN: "))
        if ppsn == "Entered PPSN is not valid":
            print(ppsn)
            print("Return to continue...")
            input()
        else:
            account_type = self.account_type_menu()
            if account_type == "deposit":
                overdraft = "False"
                while balance == False:
                    try:
                        balance = float(input("Initial Deposit: "))
                    except:
                        print("Invalid deposit value. Please enter a numeric value...")
                    while balance < 50:
                        print("The minimum initial deposit for a deposit account is €50")
                        balance = float(input("Enter initial Deposit: "))
            else:
                overdraft = input("Overdraft (y/n): ").lower()
                while (not (overdraft == "y" or overdraft == "n")): 
                    overdraft = input("Overdraft (y/n): ").lower()
                if overdraft == "y":
                    overdraft = "True"
                else:
                    overdraft = "False"
                while balance == False:
                    try:
                        balance = float(input("Initial Deposit: "))
                    except:
                        print("Invalid deposit value. Please enter a numeric value...")
                    while balance < 25:
                        print("The minimum initial deposit for a deposit account is €25")
                        balance = float(input("Enter initial Deposit: "))

            customer_account = CustomerAccount(forename, surname, ppsn, account_type, overdraft, balance)

            ds.add_customer(customer_account)

            print("Return to continue...")
            input()

    

    def validate_name(self, name):
        
        while (not name.replace(" ", "").isalpha()):
            print('')
            print('This field cannot be left empty or contain numeric values\n')
            try:
                name = input("Enter a valid name:\n")
            except ValueError:
                name = input('Please enter a name:\n')
        return name
    
    def validate_surname(self, surname):
        
        while (not surname.replace(" ", "").isalpha()):
            print('')
            print('This field cannot be left empty or contain numeric values\n')
            try:
                surname = input("Enter a valid surname:\n")
            except ValueError:
                surname = input('Please enter a surname:\n')
        return surname

    def validate_ppsn(self, ppsn):
        print("PPSN entered is: " + ppsn)
        while (not (len(ppsn) == 9 or len(ppsn) == 8 )):
                print('PPSN must contain 7 numeric charachters, and 1 or 2 check characters (letters) in the end. Ex.: 1234567wa \n')
                try:
                    ppsn = input("Enter a valid PPSN:\n")
                except ValueError:
                    ppsn = input('Please enter a PPSN:\n')
         
        numbers = ppsn[0:7]
        letters = ppsn[7:]

        if numbers.isdigit() and letters.isalpha():
            return ppsn 
        else:
            ppsn = "Entered PPSN is not valid"
            return ppsn
    

    def load_customer_account(self, account_number, customer_accounts_list):
        found = False
        for customer_account in customer_accounts_list:
            if customer_account.account_number == account_number:
                found = True
                account = customer_account
        if found == False:
            account = "Account not found"
            print(account)
            print(" ")
            print("Return to go back to main menu...")
            input()
            return account
        else:
            return account
                
    def deposit_amount(self):
        
        try:
            amount = float(input("Please, enter the amount you wish to deposit:\n"))
        except ValueError:
            amount = float(input('Please enter a number:\n'))

        while (not amount > 0):
            print('')
            print('The amount must be a number greater than 0\n')
            try:
                amount = float(input("Enter a valid amount:\n"))
            except ValueError:
                amount = float(input('Please enter a number:\n'))
        return amount
    
    def withdrawal_amount(self):
        
        try:
            amount = float(input("Please, enter the amount you wish to withdrawal:\n"))
        except ValueError:
            amount = float(input('Please enter a number:\n'))

        while (not amount > 0):
            print('')
            print('The amount must be a number greater than 0\n')
            try:
                amount = float(input("Enter a valid amount:\n"))
            except ValueError:
                amount = float(input('Please enter a number:\n'))
        return amount

    def transfer_amount(self):
        
        try:
            amount = float(input("Please, enter the amount to be transfered:\n"))
        except ValueError:
            amount = float(input('Please enter a number:\n'))

        while (not amount > 0):
            print('')
            print('The amount must be a number greater than 0\n')
            try:
                amount = float(input("Enter a valid amount:\n"))
            except ValueError:
                amount = float(input('Please enter a number:\n'))
        
        return amount

    def deposit(self, customer_account, amount):
        
        customer_account.balance += amount
        print(" ")
        print(f"Deposit of {amount} in now added to account {customer_account.account_number} balance.")
        print("------------------------")
        input("Return to continue...")
        
    
    def withdrawal(self, customer_account, amount): 
          
        if customer_account.overdraft == True:
            if amount <= 400.00:
                customer_account.balance -= amount
                print(" ")
                print("Withdrawal authorized. You can release the money now")
                print("------------------------")
                input("Return to continue...")
            else:
                print(" ")
                print("Withdrawal off limits")
                print("------------------------ ")
                input("Return to continue...")
    
        else:
            if amount <= customer_account.balance and amount <=400:
                customer_account.balance -= amount
                print(" ")
                print("Withdrawal authorized. You can release the money now")
                print("------------------------")
                input("Return to continue...")
            
            else:
                print(" ")
                print("Withdrawal off limits")
                print("------------------------ ")
                input("Return to continue...")
        
    def transfer(self, account_from, account_to, amount):

        if account_from.overdraft == True:
            account_from.balance -= amount
            account_to.balance += amount
            print(" ")
            print(f"Transfer of {amount} from account {account_from.account_number} to {account_to.account_number} completed.")
            print("------------------------")
            input("Return to continue...")
        else:
            if amount < account_from.balance:
                account_from.balance -= amount
                account_to.balance += amount
                print(" ")
                print(f"Transfer of {amount} from account {account_from.account_number} to {account_to.account_number} completed.")
                print("------------------------")
                input("Return to continue...")
            else:
                print(" ")
                print("Transfer off limits.")
                print("------------------------ ")
                input("Return to continue...")






                