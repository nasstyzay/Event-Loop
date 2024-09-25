import sqlite3

def create_tables():
    conn = sqlite3.connect('starwars.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY,
            birth_year TEXT,
            eye_color TEXT,
            films TEXT,
            gender TEXT,
            hair_color TEXT,
            height TEXT,
            homeworld TEXT,
            mass TEXT,
            name TEXT,
            skin_color TEXT,
            species TEXT,
            starships TEXT,
            vehicles TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
