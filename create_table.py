import sqlite3

def create_table():
    try:
        # Connect to the database
        conn = sqlite3.connect('instance/dados.db')
        cursor = conn.cursor()
        
        # Create the table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperatura REAL NOT NULL,
                corrente REAL NOT NULL,
                vibracao_base REAL NOT NULL,
                vibracao_braco REAL NOT NULL,
                data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Commit the changes
        conn.commit()
        print("Table 'dados' successfully created.")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
    create_table() 