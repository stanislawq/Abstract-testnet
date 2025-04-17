import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("accounts.db")
cursor = conn.cursor()

cursor.execute("SELECT private_key, faucet_last_used FROM accounts")
records = cursor.fetchall()

for record in records:
    print(f"Private Key: {record[0]}, Last Used: {record[1]}")
