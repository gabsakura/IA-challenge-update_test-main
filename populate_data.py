import sqlite3
import random
from datetime import datetime, timedelta

def populate_database():
    try:
        # Connect to the database
        conn = sqlite3.connect('instance/dados.db')
        cursor = conn.cursor()
        
        # Get current year
        current_year = datetime.now().year
        
        # Create start and end dates for the current year
        start_date = datetime(current_year, 1, 1)
        end_date = datetime(current_year, 12, 31)
        
        # Times for the 6 daily readings (in 24h format)
        daily_times = ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00']
        
        # Prepare the insert statement
        insert_query = '''
            INSERT INTO dados (temperatura, vibracao_base, vibracao_braco, corrente, data_registro)
            VALUES (?, ?, ?, ?, ?)
        '''
        
        # Generate data for each day
        current_date = start_date
        while current_date <= end_date:
            for time_str in daily_times:
                # Generate random values within limits
                temperatura = round(random.uniform(25, 47), 2)  # Between 20 and 40 degrees
                vibracao_base = round(random.uniform(1, 7), 2)  # Between 0 and 4
                vibracao_braco = round(random.uniform(1, 7), 2)  # Between 0 and 4
                corrente = round(random.uniform(2, 6), 2)  # Between 0 and 4

                # Create timestamp
                timestamp = f"{current_date.strftime('%Y-%m-%d')} {time_str}:00"
                
                # Insert the data
                cursor.execute(insert_query, (temperatura, vibracao_base, vibracao_braco, corrente, timestamp))
            
            # Move to next day
            current_date += timedelta(days=1)
        
        # Commit the changes
        conn.commit()
        print("Database successfully populated with data for the entire year.")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
    populate_database() 