import sqlite3
import json
from flask import jsonify
import pandas as pd
from ai_functions import generate_questions_claude

class SQLiteCalls:
    def __init__(
            self,
            db_path="sqlite.db"
    ):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.db_path)


#!!!!!!!!!!!!
#CHANGED ALL PRIMARY KEY AUTOINCREMENT    --- FROM --- AUTO_INCREMENT PRIMARY KEY
        conn.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT,
                generated BOOLEAN DEFAULT 0,
                common BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                is_saved BOOLEAN DEFAULT 0,
                PRIMARY KEY (user_id, question_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (question_id) REFERENCES questions (question_id)
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INT,
                answer_text TEXT,
                score INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions (question_id)
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role VARCHAR(255),
                message TEXT,
                embedding TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        conn.close()


    def assign_question(self, data):
        try:
            print('\n\n',data,'\n\n')
            question_id = data.get('question_id')
            user_id = data.get('user_id')
            if question_id is None or user_id is None:
                return jsonify({'error': 'Missing question_id or user_id parameter'}), 400
        
            try:
                question_id = int(question_id)
                user_id = int(user_id)
            except ValueError:
                return jsonify({'error': 'Invalid question_id or user_id parameter'}), 400

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 1 FROM user_questions WHERE user_id = ? AND question_id = ?
            """, (user_id, question_id))
            if cursor.fetchone():
                cursor.execute("""
                    UPDATE user_questions
                    SET is_saved = 1
                    WHERE user_id = ? AND question_id = ?
                """, (user_id, question_id))
            else:
                cursor.execute("""
                    INSERT INTO user_questions (user_id, question_id, is_saved)
                    VALUES (?, ?, 1)
                """, (user_id, question_id))

            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'Question assigned successfully', 'question_id': question_id}), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Internal Server Error'}), 500
        
    def save_question(self, data):
        try:
            question_text = data.get('question_text')
            user_id = data.get('user_id')
            is_generated = data.get('is_generated')
            is_common = data.get('is_common')
            print('\ndata in save_question\n',data,'\n\n')
            if not question_text:
                return jsonify({'error': 'Missing question_text parameter'}), 400

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO questions (question_text, generated, common)
                VALUES (?, ?, ?)
            """, (question_text, is_generated, is_common, ))
            question_id = cursor.lastrowid

            if is_generated:
                is_saved = False
            else:
                is_saved = True
            cursor.execute("""
                INSERT INTO user_questions (user_id, question_id, is_saved)
                VALUES (?, ?, ?)
            """, (user_id, question_id, is_saved, ))

            conn.commit()
            cursor.close()
            conn.close()
            return ({'question_text': question_text, 'question_id': question_id}), 200
        except Exception as e:
            print(f"Error: {e}") 
            return jsonify({'error': 'Internal Server Error'}), 500
        
    def unassign_question(self, data):
        try:
            question_id = data.get('question_id')
            user_id = data.get('user_id')

            if not question_id or not user_id:
                return jsonify({'error': 'Missing question_id or user_id parameter'}), 400

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE user_questions
                SET is_saved = 0
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

    def load_questions(self, user_id: int):
        conn = sqlite3.connect(self.db_path)
        try:
            query = """
                SELECT q.*, uq.is_saved
                FROM questions q
                LEFT JOIN user_questions uq ON q.question_id = uq.question_id AND uq.user_id = ?
                WHERE uq.user_id = ? OR uq.user_id = 2 OR q.common = 1
            """
            df = pd.read_sql_query(query, conn, params=(user_id, user_id ))
        finally:
            conn.close()
        return df

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

    # def get_questions(self, user_id: int):
    #     conn = sqlite3.connect(self.db_path)
    #     try:
    #         query = """
    #             SELECT q.*
    #             FROM questions q
    #             LEFT JOIN user_questions uq ON q.question_id = uq.question_id
    #             WHERE uq.user_id = 5
    #             AND q.question_id NOT IN (
    #                 SELECT question_id
    #                 FROM user_questions
    #                 WHERE user_id = ?
    #             )
    #         """
    #         df = pd.read_sql_query(query, conn, params=(user_id,))
    #     finally:
    #         conn.close()
    #     return df



#---------------------NEW-------------------------

    # def save_generated_user_question(self, question_text, user_id):
    #     try:
    #         # question_text = question.get('question_text')
    #         if not question_text:
    #             return jsonify({'error': 'Missing question_text parameter'}), 400

    #         conn = sqlite3.connect(self.db_path)
    #         cursor = conn.cursor()
    #         cursor.execute("""
    #             INSERT INTO generated_questions (question_text)
    #             VALUES (?)
    #         """, (question_text,))
    #         question_id = cursor.lastrowid

    #         cursor.execute("""
    #             INSERT INTO generated_user_questions (user_id, question_id)
    #             VALUES (?, ?)
    #         """, (user_id, question_id))

    #         conn.commit()
    #         cursor.close()
    #         conn.close()
    #         return jsonify({'message': 'Question saved successfully', 'question_id': question_id}), 200
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return jsonify({'error': 'Internal Server Error'}), 500
        
    # def get_generated_questions(self, user_id: int):
    #     conn = sqlite3.connect(self.db_path)
    #     try:
    #         query = """
    #             SELECT q.*
    #             FROM generated_user_questions q
    #             JOIN user_questions uq ON q.question_id = uq.question_id
    #             WHERE uq.user_id = ?
    #         """
    #         df = pd.read_sql_query(query, conn, params=(user_id,))
    #     finally:
    #         conn.close()
    #     return df
    
#------------------------END-------------------------------


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
                print('\n\n',user,'\n\n')
                # I HAD TO CHANGE THE INDEX OF THE USER_ID, MAYBE 
                # THE DATABASE SCHEMA CHANGED WHEN I DELETED THE OLD ONE
                return jsonify({'message': 'Login successful', 'id': user[3]}), 200  
            else:
                return jsonify({'error': 'Invalid username or password'}), 400
        except Exception as e:
            print(f"Error: {e}")
    

    # __________________________NEW_____________________________

    def generate_questions(self, data):
        user_id = data.get('user_id')
        user_questions = self.load_questions(user_id)

        questions = generate_questions_claude(user_questions, data)
        print('\n\n',questions,'\n\n\n')
        return_vals = []
        for question in questions:
            obj = {
                "question_text": question['question_text'],
                'user_id': user_id,
                'is_generated': True,
                'is_common': False
            }
            print('\nquestion:', obj, '\n')
            return_vals.append(self.save_question(obj))
            # print(question)
        return return_vals
