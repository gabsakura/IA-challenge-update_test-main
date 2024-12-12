import sqlite3

def delete_table():
    try:
        # Connect to the database
        conn = sqlite3.connect('instance/dados.db')
        cursor = conn.cursor()
        
        # Drop the table
        cursor.execute('DROP TABLE IF EXISTS dados')
        
        # Commit the changes and close the connection
        conn.commit()
        print("Table 'dados' successfully deleted.")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
    delete_table() 