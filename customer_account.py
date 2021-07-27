class CustomerAccount:

    next_account_number = 10203000

    #contructor
    def __init__(self, forename, surname, ppsn, account_type, overdraft, balance, interest_rate = 0.02):

        self._account_number = str(CustomerAccount.next_account_number)
        CustomerAccount.next_account_number = CustomerAccount.next_account_number + 1

        self._forename = forename
        self._surname = surname 
        self._ppsn = ppsn
        self._account_type = account_type
        self._overdraft = overdraft
        self._balance = float(balance)
        self._interest_rate = interest_rate
             

        
    
    def __repr__(self):
            repr = f"{str(self.account_number).ljust(15)} {self.forename.ljust(12)} {self.surname.ljust(12)} {self.ppsn.ljust(13)} "
            repr = repr + f"{self.account_type.ljust(15)} {self.overdraft.ljust(18)} {str(self.interest_rate).ljust(13)} {self.balance:.2f}  "
            return repr

    def file_text(self):
            return f"{self.forename}|{self.surname}|{self.ppsn}|{self.account_type}|{self.overdraft}|{self.balance:.2f}" 
        
    @property
    def account_number(self):
        return self._account_number

    @property
    def forename(self):
        return self._forename

    @forename.setter
    def forename(self, new_forename):
        self._forename = new_forename

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, new_surname):
        self._surname = new_surname

    @property
    def ppsn(self):
        return self._ppsn

    @ppsn.setter
    def ppsn(self, new_ppsn):
        self._ppsn = new_ppsn
    
    
    @property
    def account_type(self):
        return self._account_type

    @account_type.setter
    def account_type(self, new_account_type):
        self.account_type = new_account_type

    @property
    def overdraft(self):
        return self._overdraft

    @overdraft.setter
    def overdraft(self, new_overdraft):
        self._overdraft = new_overdraft

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, new_balance):
        self._balance = new_balance
    
    @property
    def interest_rate(self):
        return self._interest_rate

    @interest_rate.setter
    def interest_rate(self, new_interest_rate):
        self._interest_rate = new_interest_rate

    
    def update_interest_rate(self, account, balance):
        if account.balance > 10000:
            account.interest_rate = 0.05
        else:
            account.interest_rate = 0.02
            return account.interest_rate
        
