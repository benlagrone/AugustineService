import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MySQL connection details from environment variables
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASS = os.getenv('MYSQL_PASS')
MYSQL_DB = os.getenv('MYSQL_DB')

def setup_database():
    connection = None
    try:
        # First, connect without specifying a database to create it if it doesn't exist
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
            print(f"Database '{MYSQL_DB}' created or already exists.")
            
            # Switch to the database
            cursor.execute(f"USE {MYSQL_DB}")
            
            # Create chat_ui_history table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS chat_ui_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(64),
                session_id VARCHAR(64),
                role ENUM('user', 'assistant'),
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_table_query)
            print("Table 'chat_ui_history' created or already exists.")
            
            # Create chat_sessions table
            create_sessions_table_query = """
            CREATE TABLE IF NOT EXISTS chat_sessions (
                session_id VARCHAR(64) PRIMARY KEY,
                user_id VARCHAR(64),
                persona VARCHAR(32),
                mode VARCHAR(32),
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_active DATETIME DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE
            )
            """
            cursor.execute(create_sessions_table_query)
            print("Table 'chat_sessions' created or already exists.")
            
            connection.commit()
            print("Database setup completed successfully!")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    print("Starting database setup...")
    setup_database()