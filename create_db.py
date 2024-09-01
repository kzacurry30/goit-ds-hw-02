import sqlite3

def create_db():

    conn = sqlite3.connect('task_management.db')
    cur = conn.cursor()

    sql = '''
    

'''
    cur.executescript(sql)


    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()

conn = sqlite3.connect('task_management.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
''')


conn.commit()


conn = sqlite3.connect('task_management.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE
    )
''')


conn.commit()

conn = sqlite3.connect('task_management.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
''')


conn.commit()
