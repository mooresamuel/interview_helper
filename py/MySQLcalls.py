import mysql.connector
import json
from flask import request, jsonify
import pandas as pd

class MySQLCalls:
    def __init__(self, db_config):
        self.db_config = db_config
        self.setup_database()

    def setup_database(self):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                question_id INT AUTO_INCREMENT PRIMARY KEY,
                question_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_questions (
                user_id INT,
                question_id INT,
                PRIMARY KEY (user_id, question_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (question_id) REFERENCES questions (question_id)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                answer_id INT AUTO_INCREMENT PRIMARY KEY,
                question_id INT,
                answer_text TEXT,
                score INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions (question_id)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                role VARCHAR(255),
                message TEXT,
                embedding TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        cursor.close()
        conn.close()

    def save_question(self, data):
        try:
            question_text = data.get('question')
            if not question_text:
                return jsonify({'error': 'Missing question_text parameter'}), 400

            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO questions (question_text)
                VALUES (%s)
            """, (question_text,))
            question_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'Question saved successfully', 'question_id': question_id}), 200
        except Exception as e:
            print(f"Error: {e}")  # Print the error to the server logs
            return jsonify({'error': 'Internal Server Error'}), 500
        
    def save_user_question(self, data):
        try:
            question_text = data.get('question')
            user_id = data.get('user_id')
            if not question_text:
                return jsonify({'error': 'Missing question_text parameter'}), 400

            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO questions (question_text)
                VALUES (%s)
            """, (question_text,))
            question_id = cursor.lastrowid
            
        # Insert the question_id and user_id into the user_questions table
            cursor.execute("""
                INSERT INTO user_questions (user_id, question_id)
                VALUES (%s, %s)
            """, (user_id, question_id))
                
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'Question saved successfully', 'question_id': question_id}), 200
        except Exception as e:
            print(f"Error: {e}")  # Print the error to the server logs
            return jsonify({'error': 'Internal Server Error'}), 500

    def save_answer(self, question_id: int, answer_text: str, score: int):
        conn = mysql.connector.connect(**self.db_config)
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO answers (question_id, answer_text, score)
                VALUES (%s, %s, %s)
            """, (question_id, answer_text, score))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def get_questions(self, user_id: int):
        conn = mysql.connector.connect(**self.db_config)
        try:
            query = """
                SELECT q.*
                FROM questions q
                LEFT JOIN user_questions uq ON q.question_id = uq.question_id
                WHERE uq.user_id = 0
                AND q.question_id NOT IN (
                    SELECT question_id
                    FROM user_questions
                    WHERE user_id = %s
            )
            """
            df = pd.read_sql_query(query, conn, params=(user_id,))
        finally:
            conn.close()
        return df

    def get_user_questions(self, user_id: int):
        conn = mysql.connector.connect(**self.db_config)
        try:
            query = """
                SELECT q.*
                FROM questions q
                JOIN user_questions uq ON q.question_id = uq.question_id
                WHERE uq.user_id = %s
            """
            df = pd.read_sql_query(query, conn, params=(user_id,))
        finally:
            conn.close()
        return df

    def save_user(self, data):
        try:
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            existing_user = cursor.fetchone()
            if existing_user:
                if existing_user[1] == username:
                    return jsonify({'error': 'Username already exists'}), 400
                if existing_user[2] == email:
                    return jsonify({'error': 'Email already exists'}), 400
            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'User registered successfully'}), 200
        except Exception as e:
            print(f"Error: {e}")  # Print the error to the server logs
            return jsonify({'error': 'Internal Server Error'}), 500

    def login(self, data):
        try:
            username = data.get('username')
            password = data.get('password')

            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                return jsonify({'message': 'Login successful', 'id': user[0]}), 200
            else:
                return jsonify({'error': 'Invalid username or password'}), 400
        except Exception as e:
            print(f"Error: {e}")

    def save_message(self, role: str, message: str, embedding):
        conn = mysql.connector.connect(**self.db_config)
        try:
            cursor = conn.cursor()
            embedding_str = json.dumps(embedding) if not isinstance(embedding, str) else embedding

            cursor.execute("""
                INSERT INTO chat_history (role, message, embedding)
                VALUES (%s, %s, %s)
            """, (role, message, embedding_str))

            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def load_chat_to_dataframe(self, role=""):
        conn = mysql.connector.connect(**self.db_config)
        try:
            if role == "user" or role == "assistant":
                df = pd.read_sql_query('''
                    SELECT role, message, embedding, date FROM chat_history
                    WHERE role = %s
                    ORDER BY date ASC
                ''', conn, params=(role,))
            else:
                df = pd.read_sql_query('''
                    SELECT * FROM chat_history
                    ORDER BY date ASC
                ''', conn)
        finally:
            conn.close()
        return df