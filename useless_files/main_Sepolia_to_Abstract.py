import sqlite3
from Network import Sepolia
from client import Client


def get_wallets_from_db():
    with sqlite3.connect('/accounts.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT private_key FROM accounts")
        wallets = cursor.fetchall()

    return [wallet[0] for wallet in wallets]


def update_successful_bridge(private_key, DB_PATH='C:\\Users\\Stanislav\\PycharmProjects\\SepoliaBridge\\accounts.db'):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE accounts
            SET SepoliaToAbstract_successful_bridges = SepoliaToAbstract_successful_bridges + 1
            WHERE private_key = ?
        """, (private_key,))
        conn.commit()


def update_failed_bridge(private_key, DB_PATH='C:\\Users\\Stanislav\\PycharmProjects\\SepoliaBridge\\accounts.db'):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE accounts
            SET SepoliaToAbstract_failed_bridges = SepoliaToAbstract_failed_bridges + 1
            WHERE private_key = ?
        """, (private_key,))
        conn.commit()


def get_balance(private_key, DB_PATH='C:\\Users\\Stanislav\\PycharmProjects\\SepoliaBridge\\accounts.db'):
    client = Client(private_key, Sepolia)

    balance_wei = client.get_balance()
    balance_eth = round((balance_wei / 10 ** 18), 5)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE accounts
            SET balance_SepoliaETH = ?
            WHERE private_key = ?
        """, (balance_eth, private_key))
        conn.commit()


def bridge_wallets():
    wallets = get_wallets_from_db()

    for private_key in wallets:
        try:
            client = Client(private_key, Sepolia)

            client.bridge_eth(chain=Sepolia, value=0.001)
            print(f"Bridge successful for wallet: {private_key}\n")

            update_successful_bridge(private_key)
            get_balance(private_key)

        except Exception as e:
            update_failed_bridge(private_key)
            get_balance(private_key)
            print(f"Error processing wallet {private_key}: {e}\n")


if __name__ == "__main__":
    bridge_wallets()
