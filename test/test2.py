import sqlite3


def get_wallets_from_db():

    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT private_key FROM accounts")
    wallets = cursor.fetchone()
    conn.close()
    return wallets





def update_successful_bridge(private_key, DB_PATH = 'test.db'):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE accounts
        SET successful_bridges = successful_bridges + 1
        WHERE private_key = ?
    """, (private_key,))

    conn.commit()
    conn.close()


wallets = get_wallets_from_db()
print(wallets)
for private_key in wallets:

    update_successful_bridge(private_key)



