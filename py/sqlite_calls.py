import sqlite3
import json
from flask import request, jsonify

import pandas as pd


class SQLiteCalls:
    def __init__(
            self,
            db_path="sqlite.db"
    ):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.db_path)

        # cursor = conn.cursor()
        # cursor.execute('DROP TABLE IF EXISTS chat_history')
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_questions (
                user_id INTEGER,
                question_id INTEGER,
                PRIMARY KEY (user_id, question_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (question_id) REFERENCES questions (question_id)
            );
        """)
                     
        # Create answers table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER,
                answer_text TEXT,
                score INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions (question_id)
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                message TEXT,
                embedding TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

    def save_question(self, data):
        try:

            print(f"Received data: {data}")  # Debugging statement
            question_text = data.get('question')

            if not question_text:
                return jsonify({'error': 'Missing question_text parameter'}), 400
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO questions (question_text)
                VALUES (?)
            """, (question_text,))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Question saved successfully'}), 200
        except Exception as e:
            print(f"Error: {e}")  # Print the error to the server logs
            return jsonify({'error': 'Internal Server Error'}), 500

    def save_answer(self, question_id: int, answer_text: str, score: int):
        conn = sqlite3.connect(self.db_path, timeout=5)
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO answers (question_id, answer_text, score)
                VALUES (?, ?, ?)
            """, (question_id, answer_text, score))
            conn.commit()
        finally:
            conn.close()
    
    def get_questions(self):
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query("SELECT * FROM questions", conn)
        return df

    def get_user_questions(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            query = """
                SELECT q.*
                FROM questions q
                JOIN user_questions uq ON q.question_id = uq.question_id
                WHERE uq.user_id = ?
            """
            df = pd.read_sql_query(query, conn, params=(user_id,))
        return df
    
    def save_user(self, data):
        try:
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
            existing_user = cursor.fetchone()
            if existing_user:
                if existing_user[1] == username:
                    return jsonify({'error': 'Username already exists'}), 400
                if existing_user[2] == email:
                    return jsonify({'error': 'Email already exists'}), 400
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            conn.commit()
            conn.close()
            return jsonify({'message': 'User registered successfully'}), 200
        except Exception as e:
            print(f"Error: {e}")  # Print the error to the server logs
            return jsonify({'error': 'Internal Server Error'}), 500

    def login(self, data):
        try:
            username = data.get('username')
            password = data.get('password')

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            conn.close()
            if user:
                return jsonify({'message': 'Login successful', 'id': user[0]}), 200
            else:
                return jsonify({'error': 'Invalid username or password'}), 400
        except Exception as e:
            print(f"Error: {e}")





    def save_message(self, role: str, message: str, embedding):
        conn = sqlite3.connect(self.db_path, timeout=5)
        try:
            cursor = conn.cursor()
            embedding_str = json.dumps(embedding) if not isinstance(embedding, str) else embedding

            cursor.execute("""
                INSERT INTO chat_history (role, message, embedding)
                VALUES (?, ?, ?)
            """, (role, message, embedding_str))

            conn.commit()
        finally:
            conn.close()

    def load_chat_to_dataframe(self, role=""):
        conn = sqlite3.connect(self.db_path, timeout=5)
        try:
            if role == "user" or role == "assistant":
                df = pd.read_sql_query('''
                    SELECT role, message, embedding, date FROM chat_history
                    WHERE role = ? 
                    ORDER BY date ASC                
                ''', conn, params=(role, ))
            else:
                df = pd.read_sql_query('''
                    SELECT * FROM chat_history
                    ORDER BY date ASC                
                ''', conn)
        finally:
            conn.close()
        return df
