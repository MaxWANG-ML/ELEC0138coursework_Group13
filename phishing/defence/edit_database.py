import sqlite3
import datetime

DB_PATH = "blacklist.db"

# Path to the database file
DB_PATH = "blacklist.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blacklist (
            domain TEXT PRIMARY KEY,
            added_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def is_domain_in_blacklist(domain):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT domain FROM blacklist WHERE domain = ?", (domain,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_domain_to_blacklist(domain):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cursor.execute("INSERT OR IGNORE INTO blacklist (domain, added_time) VALUES (?, ?)", (domain, now))
    conn.commit()
    conn.close()


def delete_domain(domain):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM blacklist WHERE domain = ?", (domain,))
    conn.commit()
    conn.close()
    print(f"Domain {domain} has been deleted from the database.")


def delete_all_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM blacklist")
    conn.commit()
    conn.close()
    print("All data has been deleted from the database.")

# Example usage
if __name__ == "__main__":
    delete_all_data()
