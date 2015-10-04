import sqlite3

def insert_into_db(db_name, questions):
    print 'Inserting into database ' + db_name + '...'
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS questions
                 (text text, description text, link text,
                               UNIQUE(text))''')

    c.executemany('INSERT OR IGNORE INTO questions VALUES (?, ?, ?)', questions)

    conn.commit()
    conn.close()
