# mysql_memory.py

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load MySQL connection variables from environment variables
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASS = os.getenv('MYSQL_PASS')
MYSQL_DB = os.getenv('MYSQL_DB')

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=MYSQL_DB
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def store_chat_message(user_id, session_id, role, message):
    """Store a chat message in the database."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO chat_ui_history (user_id, session_id, role, message)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, session_id, role, message))
            connection.commit()
            print("Message stored successfully")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

def retrieve_chat_history(session_id):
    """Retrieve chat history for a session."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM chat_ui_history WHERE session_id = %s"
            cursor.execute(query, (session_id,))
            records = cursor.fetchall()
            return records
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            connection.close()