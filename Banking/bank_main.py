import bank_class as bc
import create_db as cdb
import sqlite3

tables = ('Customer','Account','Transaction')
data_inserted = False
mybank = None


def create_objects():
    bank_name = input('Please enter your bank name: \n>')
    bank_s_money = input('Please enter your starting money: \n>')
    global mybank
    mybank = bc.Bank(bank_name,bank_s_money)
    print('Bank object created successfully')

    for table in tables:
        print('\n',table)
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        query = f"""
SELECT * FROM '{table}'           
"""
        cursor.execute(query)
        for row in cursor.fetchall():
            print(row)
            if table == 'Customer':
                customer_id, name, contact, username,password = row
                customer_obj = bc.Customer(customer_id, name, contact, username,password)
                mybank.customers_[customer_id] = customer_obj

            elif table == 'Account':
                account_id, customer_id, name, balance = row
                if customer_id in mybank.customers_.keys():
                    account_obj = bc.Account(account_id, customer_id, name, balance)
                    (mybank.customers_[customer_id]).accounts_[account_id] = account_obj                
                
            elif table == 'Transaction':
                if len(row) == 5:
                    transaction_id, account_id, amount, type_, recipient = row
                else: 
                    transaction_id, account_id, amount, type_ = row
                    recipient = ''
                transaction_tpl = (transaction_id, account_id, amount, type_, recipient)
                for customer in mybank.customers_.values():
                    if account_id in customer.accounts_:
                        customer.accounts_[account_id].transactions_.append(transaction_tpl)
                
        print(f"{table} objects created successfully\n")
    print(f"All objects created successfully\n\n")
    


if __name__ == '__main__':
    cdb.create()
    if data_inserted == False:
        cdb.insert_sample_data()
        data_inserted = True
    create_objects()
    print(str(mybank))

    # test
    for customer in mybank.customers_.values():
        for account in customer.accounts_.values():
            print(account.view_transactions())

    for customer in mybank.customers_.values():
        customer.run()
        
            
