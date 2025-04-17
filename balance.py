import sqlite3
from Network import Abstract
from client_Abstract_to_Sepolia import Client


def get_wallets_from_db():
    with sqlite3.connect('accounts.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT private_key FROM accounts")
        wallets = cursor.fetchall()

    return [wallet[0] for wallet in wallets]


def get_balance(private_key, DB_PATH='accounts.db'):
    client = Client(private_key, Abstract)

    balance_wei = client.get_balance()
    balance_eth = round((balance_wei / 10 ** 18), 5)
    print(private_key, ":", balance_eth)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE accounts
            SET balance = ?
            WHERE private_key = ?
        """, (balance_eth, private_key))
        conn.commit()


def bridge_wallets():
    wallets = get_wallets_from_db()

    for private_key in wallets:
        try:
            get_balance(private_key)
        except Exception as e:
            print(f"Error processing wallet {private_key}: {e}\n")


if __name__ == "__main__":
    bridge_wallets()
