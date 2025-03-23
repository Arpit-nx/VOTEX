import mysql.connector

class DatabaseHandler:
    def __init__(self):
        # MySQL connection configuration
        self.db_config = {
            'user': 'your_username',      # Replace with your MySQL username
            'password': 'your_password',  # Replace with your MySQL password
            'host': 'localhost',
            'database': 'speech_translations'
        }
        self.connect()

    def connect(self):
        try:
            # Initialize connection to the database
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def create_table(self):
        try:
            # Create a table if it doesn't exist
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS translations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    recognized_text TEXT,
                    translated_text TEXT,
                    audio_file_path VARCHAR(255)
                )
            ''')
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def insert_translation(self, recognized_text, translated_text, audio_file_path):
        try:
            # Insert translation into the database
            sql = "INSERT INTO translations (recognized_text, translated_text, audio_file_path) VALUES (%s, %s, %s)"
            values = (recognized_text, translated_text, audio_file_path)
            self.cursor.execute(sql, values)
            self.conn.commit()
            print("Translation inserted into the database.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close(self):
        # Close the database connection
        self.cursor.close()
        self.conn.close()
