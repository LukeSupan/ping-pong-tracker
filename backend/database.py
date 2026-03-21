import sqlite3


def get_db():
    conn = sqlite3.connect('pingpong.db')  # connection, make if not present

    # instead of returning tuples. return dictionary rows. makes things easier
    conn.row_factory = sqlite3.Row

    return conn


def init_db():
    conn = get_db()  # get connection

    # build the table.
    # probably score 1, score 2? or an array
    # probably player 1, player 2? or an array
    # itll be formatted before being put in there so its always the same player
    conn.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player1 TEXT,
                    player2 TEXT,
                    score1 INTEGER,
                    score2 INTEGER
                )
    """)

    # wrap up when done
    conn.commit()
    conn.close()
