import os
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

        # application is now exiting - write customers list to file
        file_parser = FileParser()

        file_parser.write_customer_account("cust_accounts.txt", ds.customer_accounts_list)



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
            self.create_customer_account(ds)

        elif(selection == "2"):
            amount = self.deposit_amount()
            customer_account = self.load_customer_account(input("Enter an account number: "), ds.customer_accounts_list)
            if customer_account == "Account not found":
                self.show_user_menu(ds)
            else:
                self.deposit(customer_account, amount)

        elif(selection == "3"):
            amount = self.withdrawal_amount()
            customer_account = self.load_customer_account(input("Enter account number: "), ds.customer_accounts_list)
            if customer_account == "Account not found":
                self.show_user_menu(ds)
            else:
                self.withdrawal(customer_account, amount)
        
        elif(selection == "4"):
            self.display_all_accounts(ds)
        
        elif(selection == "5"):
            self.display_specific_account(ds)

        elif(selection == "6"):
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


    def create_customer_account(self, ds):
        print("Create a new Customer Account")
        print("==================\n")
        forename = input("Forename: ")
        surname = input("Surname: ")
        ppsn = input("Enter the PPSN: ")
        account_type = input("Choose account type: ")
        overdraft = input("Overdraft (y/n): ")
        balance = False
        while balance == False:
            try:
                balance = float(input("Initial Balance: "))
            except:
                print("Invalid balance. Please enter a numeric value...")

        customer_account = CustomerAccount(forename, surname, ppsn, account_type, overdraft, balance)

        ds.add_customer(customer_account)

        print("Return to continue...")
        input()

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






                