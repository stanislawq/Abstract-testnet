from captcha import send_faucet_request
from client_Abstract_to_Sepolia import Client
from Network import Abstract
import sqlite3
import time
from datetime import datetime, timedelta
import random
import urllib3

sqlite3.register_adapter(datetime, lambda dt: dt.isoformat())
sqlite3.register_converter("timestamp", lambda s: datetime.fromisoformat(s.decode("utf-8")))
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = {
    
}


def get_accounts(db_name="accounts.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    now = datetime.now()
    twenty_four_hours_ago = now - timedelta(hours=0 )

    cursor.execute("""
            SELECT private_key FROM accounts WHERE faucet_last_used < ? OR faucet_last_used IS NULL
        """, (twenty_four_hours_ago,))

    accounts = cursor.fetchall()

    conn.close()
    return [account[0] for account in accounts]


def update_last_used(private_key, db_name="accounts.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE accounts SET faucet_last_used = ? WHERE private_key = ?
    """, (datetime.now(), private_key))

    conn.commit()
    conn.close()


def get_balance(private_key, DB_PATH='accounts.db'):
    client = Client(private_key, Abstract)

    balance_wei = client.get_balance()
    balance_eth = round((balance_wei / 10 ** 18), 5)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE accounts
            SET balance = ?
            WHERE private_key = ?
        """, (balance_eth, private_key))
        conn.commit()


def update_failed_bridge(private_key, DB_PATH="accounts.db"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE accounts
        SET failed_bridges = failed_bridges + 1
        WHERE private_key = ?
    """, (private_key,))
    conn.commit()
    conn.close()


def main():
    private_keys = get_accounts()
    for private_key_index in range(len(private_keys)):
        print('-------------------------------------------------------------')
        print(f'({private_key_index + 1}/{len(private_keys)})')
        client = Client(private_keys[private_key_index], Abstract)
        print(f'Processing account {client.address}')
        response = True #send_faucet_request(client.address, proxy, 5)
        if response:
            update_last_used(private_key=private_keys[private_key_index])
            sleep_time = random.uniform(3, 12 )
            time.sleep(sleep_time)
            balance = client.get_balance()
            balance_eth = round((balance / 10 ** 18), 5)
            print(f'Current balance: {balance} WEI / {balance_eth} ETH')
            if balance > 0:
                try:
                    random_value = random.uniform(0.00002, 0.00009)
                    tx_hash = client.bridge_eth(random_value)
                    client.verify_tx(tx_hash)
                    get_balance(private_keys[private_key_index])
                except Exception as e:
                    print('Bridge error', e)
                    update_failed_bridge(private_keys[private_key_index])


if __name__ == '__main__':
    main()
