from customer_account import CustomerAccount

class FileParser():

    def read_customer_accounts(self, filename):

        customer_accounts_list = []

        try:
            fo = open(filename, "r")

            # store the file contents as a list of strings
            lines = fo.readlines()
            fo.close()
        except IOError:
            print(f"Warning: Could not open file {filename} for reading.")
            input("Return to continue...")

            # return the empty list of customer_accounts
            return customer_accounts_list

        # parse each line of customers file and create a Customer object
        for line in lines:
            customer_account = self.parse_customer_account_text(line)
            customer_accounts_list.append(customer_account)
        
        return customer_accounts_list

    def parse_customer_account_text(self, cust_text):

        fields = cust_text.split("|")

        forename = fields[0]
        surname = fields[1]
        ppsn = fields[2]
        account_type = fields[3]
        overdraft = fields[4]
        balance = float(fields[5])

     
        return CustomerAccount(forename, surname, ppsn, account_type, overdraft, balance)
    

    def write_customer_account(self, filename, customer_accounts_list):

        # list to contain text versions of custumer_accounts for writing
        lines = []
        first_customer_account = True

        # build a list of customer_account file strings
        for customer_account in customer_accounts_list:

            if first_customer_account == True:
                lines.append(customer_account.file_text())
                first_customer_account = False
            else:
                # if this isn't the first account, add a newline before writing
                lines.append(f"\n{customer_account.file_text()}")
        
        try:
            fo = open(filename, "w")
            fo.writelines(lines)
            fo.close()
        except IOError:
            print(f"Warning: Could not open {filename} for writing")
            input("Return to continue...")
