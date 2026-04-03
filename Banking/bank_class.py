import sqlite3

class Bank:
    def __init__(self, name:str, starting_money=0.0):
        self.name_ = name
        self.customers_ = {} # id-customer_obj pair
        self.starting_money_ = float(starting_money)
    def bank_menus(self, func:str):
        # print a menu based on the respective functions 
        pass

    #getter function
    def get_name(self):
        return self.name_
    def get_starting_money(self):
        return self.starting_money_
    def get_total_money(self):
        customer_total = sum(customer.get_balance() for customer in self.customers_.values())
        return customer_total + self.get_starting_money()

    
    # other functions
    def add_customer(self):
        # ask for customer's details
        # create the customer
        # add te id-customer pair into the dictionary 
        # update the database
        # ask the customer if they would like to create an account and proceed accordingly
        pass
    def loginto_customer(self):
        # display login menu
        # get username and password
            # call the respective customer.customer_run() from the dictionary
            # return to main menu
        # else print(username or password incorrect)
        pass
    def __str__(self):
        return f"""
Bank Name: {self.get_name()}
Starting Money: ${self.get_starting_money():.2f}
Bank Balance: ${self.get_total_money():.2f}
        """
    def bank_run(self):
        # displays str(self)
        # ask if user would like to log in or quit
        # proceed accordingly
        pass


class Customer:
    def __init__(self, customer_id, name, contact, username,password): 
        self.customer_id_ = customer_id
        self.name_ = name
        self.contact_ = contact
        self.username_ = username
        self.password_ = password
        self.accounts_ = {} # id-account_obj pair
        self.id_map_ = {}
        for account in self.get_accounts().values():
            self.id_map_[account.get_name()] = account.get_account_id()

    

    # getter functions
    def get_customerId(self):
        return self.customer_id_
    def get_name(self):
        return self.name_
    def get_username(self):
        return self.username_
    def get_pswd(self):
        return self.password_
    def get_accounts(self):
        return self.accounts_
    def get_balance(self):
        return sum(account.get_balance() for account in self.accounts_.values())
    def get_acc_id(self,name):
        try: 
            return self.id_map_[name]
        except KeyError:
            return False
        
    
    def cust_menus(self,func:str):
        if func == 'run':
            print(f"""
Welcome! {self.get_name()}
What would you like to do today? 
Please select an option:
1. (A)dd account
2. (E)nter account
3. (D)elete account
4. (Q)uit
""")
        elif func == 'v':
            print(f"""
           
""")
        
    
    def add_account(self, acc_name):
        # update sql
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        query = '''
INSERT INTO 'Account'
(CustomerId,AccountName,Balance)
VALUES
(?,?,?)
'''
        cursor.execute(query,(self.get_customerId(),acc_name,0.0))
        acc_id = cursor.lastrowid
        conn.commit()
        conn.close()
        # update memory
        account_obj = Account(acc_id,self.get_customerId,acc_name,0.0)
        self.accounts_[acc_id] = account_obj
        self.id_map_[acc_name] = acc_id
        return True

    def delete_account(self, acc_id):
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        query = f'''
DELETE FROM 'Account' 
WHERE AccountID == ?
and CustomerID == ?
'''
        cursor.execute(query,(acc_id,self.get_customerId()))
        conn.commit()
        conn.close()
        # update memory
        del self.accounts_[acc_id]
        return True


    def __str__(self):
        output = f"""
Your balance: ${self.get_balance()}
Your Accounts
-----------+--------------------+-----------+
Account ID | Account Name       | Balance   |
-----------+--------------------+-----------+
"""
        for account in self.get_accounts().values():
            output += f"{account.get_account_id():<10} | {account.get_name():<18} | {account.get_balance():<9} |\n"
        return output
    

    
        #######################################
    def _handle_add_account(self):
        acc_name = input("Enter account name (R to return):\n> ").strip()

        if acc_name.lower() == 'r':
            return

        if acc_name in [acc.get_name() for acc in self.accounts_.values()]:
            print(f"Account already exists under {self.get_name()}")
            return

        if self.add_account(acc_name):
            print(f"Account '{acc_name}' added successfully")
        else:
            print("Error. Please try again")
    #####################################
    def _handle_enter_account(self):
        acc_name = input("Enter account name:\n> ").strip()
        acc_id = self.get_acc_id(acc_name)

        if not acc_id:
            print("Account does not exist. Try again")
            return

        try: 
            self.accounts_[acc_id].run()
        except KeyError:
            print('ID does not exsit in dict')
    ###################################
    def _handle_delete_account(self):
        acc_name = input("Enter account name (R to return):\n> ").strip()
        if acc_name.lower() == 'r':
            return

        acc_id = self.get_acc_id(acc_name)
        if not acc_id:
            print("Account not found")
            return

        password = input("Enter your password:\n> ").strip()
        if password != self.get_pswd():
            print("Incorrect password")
            return

        if self.delete_account(acc_id):
            del self.id_map_[acc_name]
            print(f"Account '{acc_name}' deleted successfully")
        else:
            print("Error. Please try again")

        
    def run(self):
        while True:
            print(self)
            self.cust_menus('run')
            choice = input('> ').strip().lower()

            if choice in ('q', '4'):
                return 'Q'

            elif choice in ('1', 'a'):
                self._handle_add_account()

            elif choice in ('2', 'e'):
                self._handle_enter_account()

            elif choice in ('3', 'd'):
                self._handle_delete_account()

            else:
                print("Invalid. Please select from the options")




    
        
    










class Account:
    def __init__(self, account_id, customer_id,name, balance=0.0):
        self.account_id_ = account_id
        self.customer_id_ = customer_id
        self.name_ = name
        self.balance_ = balance
        self.transactions_  = [] # list of tuples (transaction_id, account_id, amount, type, recipient)
        
    def get_account_id(self):
        return self.account_id_
    def get_customer_id(self):
        return self.customer_id_
    def get_name(self):
        return self.name_
    def get_balance(self):
        return self.balance_
    def get_transactions(self):
        return self.transactions_

    def acc_menu(self, func:str):
        if func == 'run':
            print(f"""
Account balance: ${self.get_balance():.2f}
Please select an option:
1. (D)eposit
2. (W)ithdraw
3. (T)ransfer Money
4. (V)iew Transaction History
5. (R)eturn
""")
        elif func == 'wd':
            print(f"""
Select amount to withdraw:
1. $10
2. $50
3. $100
4. $200
5. $500  
Enter (R) to return
""")
            

    def execute_transaction(self, type_, amount,recipient=''): # performs the actual transaction 
        if amount<=0:
            print("Invalid amount. Please enter a positive amount. ")
            return False
        if type_ == 'Deposit' or type_ == 'Withdraw':
            if type_ == 'Withdraw':
                if amount > self.balance_:
                    print("Insufficient funds.")
                    return False
                amount = -amount
        # update sql
        query = f"""
INSERT INTO 'Transaction' 
(AccountId,Amount,Type,Recipient)
VALUES
(?,?,?,?)
        """
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        cursor.execute(query,(self.get_account_id(),amount,type_,recipient))
        transaction_id = cursor.lastrowid # DO NOT MANUALLY GENERATE TRANSACTIONIDS, let the sql generate it and refer to it. the db is the 'master'
        conn.commit()
        conn.close()
        self.balance_ += amount # UPDATE MEMORY AFTER UPDATING DB
        # add the transaction into self.transactions
        self.transactions_.append(
            (transaction_id,self.get_account_id(), amount, type_, recipient)
        )
        return True
            

    def view_transactions(self):
        output = (f"""
Account Name: {self.get_name()}
Transaction ID | Type           | Amount      | Recipient ID |
---------------+----------------+-------------+--------------+
""")
        # print(self.get_transactions())
        for row in self.get_transactions():
            transaction_id, account_id, amount, type_, recipient = row
            output += f"{transaction_id:<14} | {type_:<14} | ${amount:<10.2f} | {recipient:<12} |\n"
        print(output)


    def run(self):
        self.acc_menu('run')
        uchoice = input('>')
        while uchoice.lower() != 'r':
            if len(uchoice) == 1 and uchoice.lower() in ('1','2','3','4','5','d','w','t','v','r'):
                if uchoice in ('1','d'):
                    try: 
                        amount = float(input('Enter amount to deposit: \n>'))
                        o_balance = self.get_balance()
                        state = self.execute_transaction('Deposit',amount)
                        n_balance = self.get_balance()
                        if state == False:
                            continue
                        print(f"""
===============================+
Initial balance   : ${o_balance:<10.2f}|
Deposit amount    : ${amount:<10.2f}|
Updated balance   : ${n_balance:<10.2f}|
===============================+
""")   
                    except ValueError: 
                        print("Invalid input. Please enter a valid number.")
                if uchoice in ('2','w'):
                    self.acc_menu('wd')
                    try: 
                        amount = float(input('>'))         
                        if amount == 'R':
                            self.acc_menu('run')
                            uchoice = input('>')
                            continue
                        if amount in (1.0,10.0):
                            amount= 10.0
                        elif amount in (2.0,50.0):
                            amount = 50.0
                        elif amount in (3.0,100.0):
                            amount = 100.0
                        elif amount in (4.0,200.0):
                            amount = 200.0
                        elif amount in (5.0,500.0):
                            amount = 500.0
                        else:
                            print("Invalid. Please select from the options above.")
                            continue
                        o_balance = self.get_balance()
                        state = self.execute_transaction('Withdraw',amount)
                        n_balance = self.get_balance()
                        if state == False:
                            print("Invalid input")
                            continue
                        else:
                            print(f"""
===============================+
Initial balance   : ${o_balance:<10.2f}|
Withdrawwl amount : ${amount:<10.2f}|
Updated balance   : ${n_balance:<10.2f}|
===============================+
""")
                    except ValueError:
                        print('Invalid input. Please enter a positive integer.') 
                if uchoice in ('3','t'):
                    print('This function is under maintenence. Thank you') # put on hold
                    self.acc_menu('run')
                    uchoice = input('>')                   
                if uchoice in ('4','v'):
                    self.view_transactions()
            else:
                print('Please select from the options')
                uchoice = input('>')
            self.acc_menu('run')
            uchoice = input('>')
        return('r')







