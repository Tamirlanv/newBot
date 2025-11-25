import sqlite3


def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    # Trello таблица
    cur.execute("""
        CREATE TABLE IF NOT EXISTS trello (
            user_id INTEGER PRIMARY KEY,
            trello_key TEXT,
            trello_token TEXT,
            board_id TEXT
        );
    """)

    # CoinGecko таблица
    cur.execute("""
        CREATE TABLE IF NOT EXISTS coingecko (
            user_id INTEGER PRIMARY KEY,
            api_key TEXT
        );
    """)

    conn.commit()
    conn.close()


# -------- Trello ----------

def save_trello_keys(user_id, key, token):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO trello (user_id, trello_key, trello_token)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            trello_key = excluded.trello_key,
            trello_token = excluded.trello_token;
    """, (user_id, key, token))
    conn.commit()
    conn.close()


def get_trello_keys(user_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT trello_key, trello_token FROM trello WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row if row else (None, None)


def save_board_id(user_id, board_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("UPDATE trello SET board_id=? WHERE user_id=?", (board_id, user_id))
    conn.commit()
    conn.close()


def get_board_id(user_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT board_id FROM trello WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


# -------- CoinGecko ----------

def save_cg_key(user_id, api_key):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO coingecko (user_id, api_key)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET api_key = excluded.api_key;
    """, (user_id, api_key))
    conn.commit()
    conn.close()


def get_cg_key(user_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT api_key FROM coingecko WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
