import sqlite3

customers = 'data/customer_data.csv'
accounts = 'data/account_data.csv'
transactions = 'data/transaction_data.csv'
data_files = [customers,accounts,transactions]

def get_filenames():
	return data_files


customer = """
CREATE TABLE IF NOT EXISTS"Customer" (
	"CustomerID"	INTEGER NOT NULL UNIQUE,
	"Name"	TEXT NOT NULL,
	"Contact"	TEXT NOT NULL,
	"Username"	TEXT NOT NULL UNIQUE,
	"Password"	TEXT NOT NULL,
	PRIMARY KEY("CustomerID" AUTOINCREMENT)
);	
"""

account= """
CREATE TABLE IF NOT EXISTS"Account" (
	"AccountID"	INTEGER NOT NULL UNIQUE,
	"CustomerID"	INTEGER NOT NULL,
	"AccountName"	TEXT NOT NULL,
	"Balance"	REAL NOT NULL,
	PRIMARY KEY("AccountID" AUTOINCREMENT),
	FOREIGN KEY("CustomerID") REFERENCES "Customer"("CustomerID")
);
"""

transactions = """
CREATE TABLE IF NOT EXISTS"Transaction" (
	"TransactionID"	INTEGER NOT NULL UNIQUE,
	"AccountID"	INTEGER NOT NULL,
	"Amount"	REAL NOT NULL,
	"Type"	TEXT NOT NULL,
	"Recipient"	TEXT,
	PRIMARY KEY("TransactionID" AUTOINCREMENT),
	FOREIGN KEY("AccountID") REFERENCES "Account"("AccountID")
);
"""

def create():
	queries = (customer,account,transactions)
	conn = sqlite3.connect('bank.db')
	for query in queries:
		conn.execute(query)
	conn.commit()
	conn.close()






















def insert_sample_data():
	conn = sqlite3.connect('bank.db')
	cursor = conn.cursor()
	cursor.execute("SELECT COUNT(*) FROM 'Customer'")
	if cursor.fetchone()[0] > 0:
		print("Data already exists, skipping insert.")
		return
	conn.close()

	for filename in data_files:
		try: 
			with open(filename,'r') as f:
				data = f.read()
				data_lines = data.split('\n')[2:]
				# print(data_lines, '\n')
				cleaned_data = [] # append into here. list of tuples (id,name,contact,username,password)
				for line in data_lines:
					items = [item.strip() for item in line.split(',')]
					cleaned_data.append(tuple(items))
				# print(cleaned_data[0])
				# print(cleaned_data[0][1])
				
				# print(('?,'*len(cleaned_data[0]))[:-1])
				query = f"""
INSERT INTO "{data.split('\n')[0]}"
VALUES
({('?,'*len(cleaned_data[0]))[:-1]})
"""
				print(query)
				conn = sqlite3.connect('bank.db')
				cursor = conn.cursor()
				for item in cleaned_data:
					cursor.execute(query, item)
				conn.commit()
				conn.close()
				print(f"Successfully inserted {data.split('\n')[0]} into databse")

		except FileNotFoundError:
			print(f'{filename} not found')

	
# create()
# insert_sample_data()