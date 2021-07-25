
from customer_account import CustomerAccount
from file_parser import FileParser

class Datastore:

    def __init__(self):

        self._customer_accounts_list = []
        #call the method that read the txt file
        self.read_customer_account()

    def read_customer_account(self):
        #instantiate a FileParser Object to read and write file
        file_parser = FileParser()
        self._customer_accounts_list = file_parser.read_customer_accounts("cust_accounts.txt")

    #def load_customers(self):

        #self._customer_accounts_list.append(Customer("yyyyyyyy", "Bbbbbb","2345672as", "12349876", "deposit", "False", 123.50))
       

    def add_customer(self, customer_account):

        self._customer_accounts_list.append(customer_account)

    @property
    def customer_accounts_list(self):
        return self._customer_accounts_list
