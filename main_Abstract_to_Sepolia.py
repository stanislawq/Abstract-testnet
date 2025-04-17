import sqlite3
from Network import Abstract
from client_Abstract_to_Sepolia import Client


def get_wallets_from_db():
    with sqlite3.connect('accounts.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT private_key FROM accounts")
        wallets = cursor.fetchall()

    return [wallet[0] for wallet in wallets]



def bridge_wallets():
    wallets = get_wallets_from_db()

    for private_key in wallets:
        try:
            client = Client(private_key, Abstract)

            client.bridge_eth(value=0.0001)
            print(f"Bridge successful for wallet: {private_key}\n")



        except Exception as e:

            print(f"Error processing wallet {private_key}: {e}\n")


if __name__ == "__main__":
    bridge_wallets()
