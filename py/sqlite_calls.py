import sqlite3
import json
from flask import jsonify
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

        conn.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                question_id INTEGER AUTO_INCREMENT PRIMARY KEY,
                question_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_questions (
                user_id INT,
                question_id INTEGER,
                PRIMARY KEY (user_id, question_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (question_id) REFERENCES questions (question_id)
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                answer_id INTEGER AUTO_INCREMENT PRIMARY KEY,
                question_id INT,
                answer_text TEXT,
                score INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions (question_id)
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER AUTO_INCREMENT PRIMARY KEY,
                role VARCHAR(255),
                message TEXT,
                embedding TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        conn.close()

    def move_into_user_questions(self, data):
        try:
            question_id = data.get('question_id')
            user_id = data.get('user_id')

            if not question_id or not user_id:
                return jsonify({'error': 'Missing question_id or user_id parameter'}), 400

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_questions (user_id, question_id)
                VALUES (?, ?)
            """, (user_id, question_id))

            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'Question saved successfully', 'question_id': question_id}), 200
        except sqlite3.Error as err:
            print(f"MySQL Error: {err}") 
            return jsonify({'error': 'Internal Server Error'}), 500
        except Exception as e:
            print(f"Error: {e}") 
            return jsonify({'error': 'Internal Server Error'}), 500

    def move_out_of_user_questions(self, data):
        try:
            question_id = data.get('question_id')
            user_id = data.get('user_id')

            if not question_id or not user_id:
                return jsonify({'error': 'Missing question_id or user_id parameter'}), 400

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM user_questions
                WHERE user_id = ? AND question_id = ?
            """, (user_id, question_id))

            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'Question removed successfully', 'question_id': question_id}), 200
        except sqlite3.Error as err:
            print(f"MySQL Error: {err}")  
            return jsonify({'error': 'Internal Server Error'}), 500
        except Exception as e:
            print(f"Error: {e}") 
            return jsonify({'error': 'Internal Server Error'}), 500

    def save_question(self, data):
        try:
            question_text = data.get('question')
            user_id = data.get('user_id')
            if not question_text:
                return jsonify({'error': 'Missing question_text parameter'}), 400


            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO questions (question_text)
                VALUES (?)
            """, (question_text,))
            question_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO user_questions (user_id, question_id)
                VALUES (?, ?)
            """, (user_id, question_id))

            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'Question saved successfully', 'question_id': question_id}), 200
        except Exception as e:
            print(f"Error: {e}") 
            return jsonify({'error': 'Internal Server Error'}), 500

    def save_user_question(self, data):
        try:
            question_text = data.get('question')
            user_id = data.get('user_id')
            if not question_text:
                return jsonify({'error': 'Missing question_text parameter'}), 400

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO questions (question_text)
                VALUES (?)
            """, (question_text,))
            question_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO user_questions (user_id, question_id)
                VALUES (?, ?)
            """, (user_id, question_id))

            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'Question saved successfully', 'question_id': question_id}), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Internal Server Error'}), 500

    def save_answer(self, question_id: int, answer_text: str, score: int):
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO answers (question_id, answer_text, score)
                VALUES (?, ?, ?)
            """, (question_id, answer_text, score))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def get_questions(self, user_id: int):
        conn = sqlite3.connect(self.db_path)
        try:
            query = """
                SELECT q.*
                FROM questions q
                LEFT JOIN user_questions uq ON q.question_id = uq.question_id
                WHERE uq.user_id = 5
                AND q.question_id NOT IN (
                    SELECT question_id
                    FROM user_questions
                    WHERE user_id = ?
            )
            """
            df = pd.read_sql_query(query, conn, params=(user_id,))
        finally:
            conn.close()
        return df

    def get_user_questions(self, user_id: int):
        conn = sqlite3.connect(self.db_path)
        try:
            query = """
                SELECT q.*
                FROM questions q
                JOIN user_questions uq ON q.question_id = uq.question_id
                WHERE uq.user_id = ?
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
            user_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 200
        except Exception as e:
            print(f"Error: {e}") 
            return jsonify({'error': 'Internal Server Error'}), 500

    def login(self, data):
        try:
            username = data.get('username')
            password = data.get('password')

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
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
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            embedding_str = json.dumps(embedding) if not isinstance(embedding, str) else embedding

            cursor.execute("""
                INSERT INTO chat_history (role, message, embedding)
                VALUES (?, ?, ?)
            """, (role, message, embedding_str))

            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def load_chat_to_dataframe(self, role=""):
        conn = sqlite3.connect(self.db_path)
        try:
            if role == "user" or role == "assistant":
                df = pd.read_sql_query('''
                    SELECT role, message, embedding, date FROM chat_history
                    WHERE role = ?
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