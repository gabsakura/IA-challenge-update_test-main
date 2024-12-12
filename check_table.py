import sqlite3

def check_table_schema():
    try:
        # Connect to the database
        conn = sqlite3.connect('instance/dados.db')
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("PRAGMA table_info(dados)")
        columns = cursor.fetchall()
        
        print("Table Schema:")
        for col in columns:
            print(f"Column: {col[1]}, Type: {col[2]}")
            
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_table_schema() 