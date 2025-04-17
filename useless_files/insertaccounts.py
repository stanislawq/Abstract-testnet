import sqlite3
import pandas as pd

conn = sqlite3.connect("../accounts.db")
cursor = conn.cursor()

csv_file = "C:\\Users\\Stanislav\\Downloads\\AbstractAccounts.csv"
df = pd.read_csv(csv_file, sep=";")

print(df.columns)

data_to_insert = df[["Address", "private_key"]].values.tolist()

cursor.executemany("INSERT INTO accounts (Address, private_key) VALUES (?, ?)", data_to_insert)

conn.commit()
conn.close()
