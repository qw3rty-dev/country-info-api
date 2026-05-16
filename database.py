import sqlite3

def get_connection():
    conn= sqlite3.connect("countries.db")
    conn.row_factory= sqlite3.Row
    return conn


def init_db():
    conn= get_connection()
    cursor= conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS country(
                   rank INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT UNIQUE,
                   population INTEGER,
                   yearly_change FLOAT,
                   net_change INTEGER,
                   density FLOAT,
                   land_area INTEGER,
                   migrants INTEGER,
                   median_age FLOAT,
                   fertility_rate FLOAT,
                   urban_pop FLOAT,
                   world_share FLOAT)
                   """)
    conn.commit()
    conn.close()