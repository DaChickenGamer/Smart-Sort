import sqlite3

# Set up the database connection and cursor
conn = sqlite3.connect('ai_file_results_test.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT NOT NULL,
        file_extension TEXT NOT NULL,
        category TEXT NOT NULL
    )
''')
conn.commit()

def add_file(file_name, file_extension, category):
    cursor.execute('''
        INSERT INTO files (file_name, file_extension, category)
        VALUES (?, ?, ?)
    ''', (file_name, file_extension, category))
    conn.commit()

def remove_file(file_id):
    cursor.execute('''
        DELETE FROM files WHERE id = ?
    ''', (file_id,))
    conn.commit()

def update_file(file_id, new_file_name, new_file_extension, new_category):
    cursor.execute('''
        UPDATE files
        SET file_name = ?, file_extension = ?, category = ?
        WHERE id = ?
    ''', (new_file_name, new_file_extension, new_category, file_id))
    conn.commit()

def get_all_files():
    cursor.execute('SELECT * FROM files')
    return cursor.fetchall()

def lookup_file_by_id(file_id):
    cursor.execute('SELECT * FROM files WHERE id = ?', (file_id,))
    return cursor.fetchone()

def lookup_files_by_name(file_name):
    cursor.execute('SELECT * FROM files WHERE file_name LIKE ?', ('%' + file_name + '%',))
    return cursor.fetchall()

def search_files(query):
    cursor.execute('''
        SELECT * FROM files 
        WHERE file_name LIKE ? OR category LIKE ?
    ''', ('%' + query + '%', '%' + query + '%'))
    return cursor.fetchall()


conn.close()
