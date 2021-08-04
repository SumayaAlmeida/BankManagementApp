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
        print("5. Search account by PPSN")
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
            print("Option 5. Search account by PPSN ")
            print("=====================================")
            self.display_account_by_ppsn(ds)

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
        
        print("Forename        Surname        Account No    Interest Rate      Balance")
        print("========================================================================")

        for customer_account in ds.customer_accounts_list:
            display_accounts = f"{customer_account.forename.ljust(15)} {customer_account.surname.ljust(15)} {customer_account.account_number.ljust(15)} "
            display_accounts = display_accounts + f"{str(customer_account.interest_rate).ljust(15)}{customer_account.balance:.2f}"
            print(display_accounts)

        print("Return to continue...")
        input()        


    def display_account_by_ppsn(self, ds):

        print("")
        accounts_found = []
        ppsn = self.validate_ppsn(input("Enter the PPSN: "))
        #search for accounts with specific ppsn and append to a list    
        for customer_account in ds.customer_accounts_list:
            if customer_account.ppsn == ppsn:
                accounts_found.append(customer_account)

        if len(accounts_found) == 0:
            print(f"No accounts found for the given PPSN: {ppsn}")
            print("Return to continue...")
            input() 

        else:
            self.clearscreen()
            print("View accounts for:")
            print("")
            print(f"PPSN: {ppsn}")
            print(f"Name: {accounts_found[0].forename} {accounts_found[0].surname}")
            print("Account No       Account type       Overdraft      Interest Rate        Balance")
            print("================================================================================")
            for account in accounts_found:
                display_accounts = f"{account.account_number.ljust(18)} {account.account_type.ljust(18)} {account.overdraft.ljust(18)} "
                display_accounts = display_accounts + f"{str(account.interest_rate).ljust(15)} {account.balance:.2f}"
                print(display_accounts)

        print("Return to continue...")
        input()     
            


    def account_type_menu(self):
        selection = "0"
        print('')
        print("Account options:")
        print("================")
        print("1. Deposit:\n Overdraft facility not available for this type of account. Opening deposit must be €50 or more.\n Type 1 to choose this type of account\n")
        print("2. Current:\n Overdraft facility is available for this type of account. Opening deposit must be €25 or more.\n Type 2 to choose this type of account\n")
        selection = ("Please choose an option (1 or 2): ")
        while(not (selection == "1" or selection == "2")):
            selection = input("Please choose an option (1 or 2): ")
        if selection == "1":
            print("")
            print("Deposit account selected. You must now deposit a minimum of €50")
            print("")
            return "deposit"
        if selection == "2":
            print("")
            print("Current account selected.")
            return "current"


    def create_customer_account(self, ds):
        forename = ""
        surname = ""
        balance = False
        ppsn_found = []
        ppsn = self.validate_ppsn(input("Enter the PPSN: "))
        if ppsn == "Entered PPSN is not valid":
            print(ppsn)
            print("Return to continue...")
            input()
        else: 
            for account in ds.customer_accounts_list:
                if account.ppsn == ppsn:
                    print(f"PPSN found. Name: {account.forename} {account.surname}")
                    forename = account.forename
                    surname = account.surname
                    ppsn_found.append(account)
            if len(ppsn_found) == 0:       
                forename = self.validate_name(input("Forename: "))
                surname = self.validate_name(input("Surname: "))
            else: 
                forename = ppsn_found[0].forename
                surname = ppsn_found[0].surname           

            account_type = self.account_type_menu()
            if account_type == "deposit":
                overdraft = "False"
                while balance == False:
                    try:
                        balance = input("Enter initial Deposit: ")
                        balance = balance.replace(",", ".")
                        balance = float(balance)
                        
                    except:
                        print("Invalid deposit value. Please enter a numeric value...")
                        balance = input("Enter initial Deposit: ")
                        balance = balance.replace(",", ".")
                        balance = float(balance)
                        
                    while balance < 50:
                        print("The minimum initial deposit for a deposit account is €50")
                        balance = input("Enter initial Deposit: ")
                        balance = balance.replace(",", ".")
                        balance = float(balance)
                        
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
                        balance = input("Enter initial Deposit: ")
                        balance = balance.replace(",", ".")
                        balance = float(balance)


                    except:
                        print("Invalid deposit value. Please enter a numeric value...")
                        balance = input("Enter initial Deposit: ")
                        balance = balance.replace(",", ".")
                        balance = float(balance)
                    while balance < 25:
                        print("The minimum initial deposit for a deposit account is €25")
                        balance = input("Enter initial Deposit: ")
                        balance = balance.replace(",", ".")
                        balance = float(balance)
                        

            customer_account = CustomerAccount(forename, surname, ppsn, account_type, overdraft, balance)
            customer_account.update_interest_rate(customer_account, balance)

            ds.add_customer(customer_account)
            print(f"Account {customer_account.account_number} sucessfully created")
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
            print('PPSN must contain 7 numeric charachters, and 1 or 2 check characters (letters) in the end. Ex.: 1234567wa')
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
            #input()
            return account
        else:
            return account
                
    def deposit_amount(self):
        
        try:
            amount = input("Please, enter the amount you wish to deposit:\n")
            amount = amount.replace(",", ".")
            amount = float(amount)
        except ValueError:
            amount = input('Please enter a number:\n')
            amount = amount.replace(",", ".")
            amount = float(amount)

        while (not amount > 0):
            print('')
            print('The amount must be a number greater than 0\n')
            try:
                amount = input("Enter a valid amount:\n")
                amount = amount.replace(",", ".")
                amount = float(amount)
            except ValueError:
                amount = input('Please enter a number:\n')
                amount = amount.replace(",", ".")
                amount = float(amount)
        return amount
    
    def withdrawal_amount(self):
        
        try:
            amount = input("Please, enter the amount you wish to withdrawal:\n")
            amount = amount.replace(",", ".")
            amount = float(amount)
        except ValueError:
            amount = input('Please enter a number:\n')
            amount = amount.replace(",", ".")
            amount = float(amount)

        while (not amount > 0):
            print('')
            print('The amount must be a number greater than 0\n')
            try:
                amount = input("Enter a valid amount:\n")
                amount = amount.replace(",", ".")
                amount = float(amount)
            except ValueError:
                amount = input('Please enter a number:\n')
                amount = amount.replace(",", ".")
                amount = float(amount)
        return amount

    def transfer_amount(self):
        
        try:
            amount = input("Please, enter the amount to be transfered:\n")
            amount = amount.replace(",", ".")
            amount = float(amount)
        except ValueError:
            amount = input('Please enter a number:\n')
            amount = amount.replace(",", ".")
            amount = float(amount)

        while (not amount > 0):
            print('')
            print('The amount must be a number greater than 0\n')
            try:
                amount = input("Enter a valid amount:\n")
                amount = amount.replace(",", ".")
                amount = float(amount)
            except ValueError:
                amount = input('Please enter a number:\n')
                amount = amount.replace(",", ".")
                amount = float(amount)
        
        return amount

    def deposit(self, customer_account, amount):
        
        customer_account.balance += amount
        customer_account.update_interest_rate(customer_account, amount)
        print(" ")
        print(f"Deposit of €{amount:.2f} in now added to account {customer_account.account_number} balance.")
        print(f"New balance is: €{round(customer_account.balance, 2)}")
        print("------------------------")
        input("Return to continue...")
        
    
    def withdrawal(self, customer_account, amount): 
          
        if customer_account.overdraft == True:
            customer_account.balance -= amount
            customer_account.update_interest_rate(customer_account, amount)
            print(" ")
            print("Withdrawal authorized. You can release the money now")
            print(f"New balance is: €{round(customer_account.balance, 2)}")
            print("------------------------")
            input("Return to continue...")
            
    
        else:
            if amount <= customer_account.balance:
                customer_account.balance -= amount
                customer_account.update_interest_rate(customer_account, amount)
                print(" ")
                print("Withdrawal authorized. You can release the money now")
                print(f"New balance is: €{round(customer_account.balance, 2)}")
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
            account_from.update_interest_rate(account_from, amount)
            account_to.balance += amount
            account_to.update_interest_rate(account_to, amount)
            print(" ")
            print(f"Transfer of {amount:.2f} from account {account_from.account_number} to {account_to.account_number} completed.")
            print(f"New balance for account {account_from.account_number}: €{round(account_from.balance, 2)}")
            print(f"New balance for account {account_to.account_number}: €{round(account_to.balance, 2)}")
            print("------------------------")
            input("Return to continue...")
        else:
            if amount < account_from.balance:
                account_from.balance -= amount
                account_from.update_interest_rate(account_from, amount)
                account_to.balance += amount
                account_to.update_interest_rate(account_to, amount)
                print(" ")
                print(f"Transfer of {amount:.2f} from account {account_from.account_number} to {account_to.account_number} completed.")
                print(f"New balance for account {account_from.account_number}: €{round(account_from.balance, 2)}")
                print(f"New balance for account {account_to.account_number}: €{round(account_to.balance, 2)}")
                print("------------------------")
                input("Return to continue...")
            else:
                print(" ")
                print("Transfer off limits.")
                print("------------------------ ")
                input("Return to continue...")

    def help(self):
        self.clearscreen()
        print("1.OPEN NEW Customer ACCOUNT in easy steps: ")
        print("===================================")
        print("   1. Enter the PPSN of the Customer.\n If The Customer already have accounts with The Green Bank forename and Surname will be automatically filled.")
        print("   2. If this is the First account enter Forename and Surname")
        print("   3. Choose account type")
        print("   4. If it is a current account choose if the customer want to add the overdraft facility by typing 'Y' for yes or 'N' for no.")
        print("   5. Enter the first deposit amount (minimum is 50 euros for Deposit account and 25 euros for current")
        print("   6. Account Created!")
        print("===================================")
        print("")
        print("2. DEPOSIT in easy steps: ")
        print("===================================")
        print("   1. Enter value that is going to be deposited into the account")
        print("   2. Count the money carefully and Enter the number of the account to be credited")
        print("   Deposit accepted!")
        print("===================================")
        print("")
        print("3. WITHDRAWAL in easy steps: ")
        print("===================================")
        print("   1. Enter a value to withdraw")
        print("   2. Enter the number of the account to be debited")
        print("   3. Wait for the System to confirm if the withdrawal amount is in the limits for this account")
        print("   4. If authorized count the money carefully before giving it to the customer")
        print("   Transaction completed")
        print("===================================")
        print("")
        print("4. VIEW all accounts in easy steps: ")
        print("===================================")
        print("   1. Just press 4 on the main menu")
        print("   2. A list of all accounts will be displayed automatically")
        print("===================================")
        print("")
        print("5.VIEW accounts by PPSN: ")
        print("===================================")
        print(" 1. Enter a valid PPSN number")
        print(" The accounts connected to the PPSN will be listed")
        print("===================================")
        print("")
        print("6. Transfer Bewtween Accounts ")
        print("=====================================")
        print("   1. Enter the AMOUNT to be transfered")
        print("   2. Enter number of the account FROM where the funds will be DEBITED")
        print("      If the amount is authorized:")
        print("   3. Enter number of the account TO where the funds will be CREDITED")
        print("      Transfer completed")
        print("===================================")
        print("")
        print("7. Online help")
        print("===================================")
        print("   From the main menu you can always choose 7 to reviews this online guide")
        print("===================================")
        print("8. Exit")
        print("===================================")
        print("   From the main menu you can always choose 8 to save changes and close the system")
        print("===================================")
        print("")
        input("Return to continue...")
        





                