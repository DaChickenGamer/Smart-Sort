import sqlite3

def get_database_connection():
    """Create and return a new database connection."""
    return sqlite3.connect('ai_file_results_test.db')

def add_file(file_path, file_extension, category, file_color):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO files (file_path, file_extension, category, file_color)
                          VALUES (?, ?, ?, ?)''', (file_path, file_extension, category, file_color))
        conn.commit()

def remove_file(file_id):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM files WHERE id = ?', (file_id,))
        conn.commit()

def update_file(file_id, new_file_path, new_file_extension, new_category, new_file_color):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE files
                          SET file_path = ?, file_extension = ?, category = ?, file_color = ?
                          WHERE id = ?''', (new_file_path, new_file_extension, new_category, new_file_color, file_id))
        conn.commit()

def get_all_files():
    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM files')
        return cursor.fetchall()

def lookup_file_by_id(file_id):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM files WHERE id = ?', (file_id,))
        return cursor.fetchone()


def lookup_files_by_file_path(file_path):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM files WHERE file_path LIKE ?', ('%' + file_path + '%',))
        rows = cursor.fetchall()

        # Convert to a list of dictionaries
        keys = ['id', 'file_path', 'file_extension', 'category', 'file_color']
        return [dict(zip(keys, row)) for row in rows]


def search_files(query):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM files WHERE file_path LIKE ? OR category LIKE ?',
                       ('%' + query + '%', '%' + query + '%'))
        return cursor.fetchall()
